"""
FILE: SundayLeague/models.py
AUTHOR: Ilay Guler (ilay2004@bu.edu)
DESCRIPTION: Relational data models which are the backbone of interaction and data-exchange for this webapp
DATE: 4/17/2026
"""

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models import Q
from django.urls import reverse

class SLProfile(models.Model):
  # Customizable athelte profile attached to an authenticated User. Ideally I would have overriden regular User auth with an abstract user, but I did not want to
  # mess with the other apps in this project which user regular user auth.
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(blank=True)
  profile_picture = models.ImageField()

  def getImageUrl(self):
    if self.profile_picture:
      return self.profile_picture.url
    else:
      return ''
    
  def getTeams(self):
    """ All teams a user-profile is a part of """
    return Team.objects.filter(teammember__user=self.user)
  
  def getUpvotes(self):
    """ Lets us gather the upvotes for a teammember """
    upvotes = Upvote.objects.filter(receiving_user = self.user)
    return upvotes

class League(models.Model):

  SPORT_CHOICES = [
        ("BB", "Basketball"),
        ("BM", "Badminton"),
        ("VB", "Volleyball"),
        ("FF", "Flag Football"),
        ("T", "Tennis"),
        ("PP", "Ping Pong"),
        ("S", "Soccer"),
        ("PB", "Pickle Ball"),
        ("SB", "Spike Ball"),
        ("WB", "Wiffle Ball"),
        ("KB", "Kickball"),
    ]

  LEVEL_CHOICES = [
      ("1", "Casual (All, or some team members should be new to this sport)"),
      ("2", "Intermediate (Most team members should be familiar and have experience with this sport)"),
      ("3", "Competitive (Most team members should be familiar and playing to win)"),
  ]
  # League is the grouping of teams for a sports league
  league_admin = models.ForeignKey(User, on_delete=models.CASCADE) # Controls league settings and can admit teams
  sport_type = models.CharField(blank=False, max_length=2, 
                                choices = SPORT_CHOICES
                                )
  is_discoverable = models.BooleanField(default=True)
  max_teams = models.IntegerField(default=10)
  league_name = models.TextField(blank=False, default='Unnamed League')
  season_start = models.DateField()
  season_end = models.DateField()
  level = models.CharField(blank=False, max_length=1,
                           choices=LEVEL_CHOICES)
  bio = models.TextField(blank=True, null=True)
  picture = models.ImageField(blank=True, null=True)

  def __str__(self):
    """ Stringified representation of a model instance """
    return ''+self.league_name + '-' +self.sport_type
  
  def getGames(self):
    """ Get all games in a league ordered by upcoming first """
    games = Game.objects.filter(league=self).order_by('time')
    return games
  
  def getTeams(self):
    """ Get all teams in a league """
    return self.teams.all()
  
  def getLeaderboard(self):
    # Checks game objects associated with this team, and whether or not they were declared winner (if there was a winner)
    teams = self.getTeams()
    wins = {}
    losses = {}

    for team in teams:
        wins[team.name] = 0
        losses[team.name] = 0

    games = self.getGames()
    for game in games:
        if game.winner is not None:
            if game.team1 != game.winner:
                losses[game.team1.name] += 1
                wins[game.team2.name] += 1
            else:
                losses[game.team2.name] += 1
                wins[game.team1.name] += 1

    return [
      {
          "team": team.name,
          "wins": wins[team.name],
          "losses": losses[team.name],
          "pk": team.pk
      }
      for team in teams
    ]
  
  def getPosts(self):
    # Gets all posts associated with this league
    posts = LeaguePost.objects.filter(league=self)
    return posts
  
  def isFull(self):
    # Indicated if the max number of teams are associated with this league
    return self.teams.count() >= self.max_teams
  
  def get_absolute_url(self):
    return reverse('detail_league', kwargs={'pk': self.pk})
  
  def getImageUrl(self):
    if self.picture:
      return self.picture.url
    else:
      return ''

class LeaguePost(models.Model):
  # Users on a team in a league can post messages to a board. 
  league = models.ForeignKey(League, on_delete=models.CASCADE)
  message = models.TextField()
  image = models.ImageField(blank=True)
  posting_user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    """ Stringified representation of a model instance """
    return ''+str(self.league) + ': ' +str(self.posting_user) + ' | ' +str(self.pk)
  
  def getImageUrl(self):
    if self.image:
      return self.image.url
    else:
      return ''

class Team(models.Model):
  # A team is a grouping of users playing in a sport league
  team_admin = models.ForeignKey(User, on_delete=models.CASCADE) # Controls team settings and can add new members
  name = models.TextField()
  leagues = models.ManyToManyField(League, related_name="teams")
  picture = models.ImageField(default=None, blank=True, null=True)
  discoverable = models.BooleanField(default=True)
  def __str__(self):  
    """ Stringified representation of a model instance """
    return 'Team:' +self.name + ' | ' + str(self.pk)
  
  def getTeamMembers(self):
    # Get members of a team
    members = TeamMember.objects.filter(team=self)
    return members
  
  def getImageUrl(self):
    if self.picture:
      return self.picture.url
    else:
      return ''
  
  def getGames(self):
    """ Get all games in a league ordered by upcoming first """
    games = Game.objects.filter((Q(team1=self) | Q(team2=self)) & Q(winner=None)).order_by('time')
    return games
    
  def getWinLosses(self):
    """ Returns dictionary of {team: str, wins: int, losses: int}"""
    """Takes the list of dictinaries for w/l and grabs the one which belongs to the team calling it"""
    default_dic = {"team": self.name, "wins":0, "losses": 0}
    for league in self.leagues.all():
      wl_dic_list = league.getLeaderboard()
      # returns something like:
      # [... {"team": "Lakers", "wins": 5, "losses": 2}, ...]
      

      for item in wl_dic_list:
        if item['team'] == self.name:
          # Error handling in case the wins/losses for a league is bunked or schema drift in the future
          if 'wins' in default_dic and 'losses' in default_dic:
            default_dic['wins'] += item['wins']
            default_dic['losses'] += item['losses']
    return default_dic


class TeamMember(models.Model):
  # Connects an authenticated user to a team
  team = models.ForeignKey(Team, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    """ Stringified representation of a model instance """
    return 'Member: '+str(self.user) + ' on ' +str(self.team)
  
  def getUpvotes(self):
    """ Lets us gather the upvotes for a teammember """
    upvotes = Upvote.objects.filter(receiving_user = self.user)
    return upvotes
  
  def getProfile(self):
    """ Lets us get the social profile for a teammember """
    profile = SLProfile.objects.get(user=self.user)
    return profile
  

class TeamJoinRequest(models.Model):
  # Object to store a request from one user to join a team
  team = models.ForeignKey(Team, on_delete=models.CASCADE)
  requesting_user = models.ForeignKey(User, on_delete=models.CASCADE)
  message = models.TextField(blank=True, null=True)

class LeagueJoinRequest(models.Model):
  # Object to store a request from one team to join a league
  league = models.ForeignKey(League, on_delete=models.CASCADE)
  requesting_team = models.ForeignKey(Team, on_delete=models.CASCADE)
  message = models.TextField(blank=True, null=True)


class Game(models.Model):
  # Connects two teams in a league, to a game scheduled at a certain time. Winner and final score are filled out when the match finishes
  league = models.ForeignKey(League, on_delete=models.CASCADE)
  time = models.DateTimeField()
  team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_1')
  team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_2')
  winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winner', blank=True, null=True)
  final_score = models.TextField(blank=True)
  location = models.TextField(blank=False, default='')

  def __str__(self):
    """ Stringified representation of a model instance """
    return 'League: ' + str(self.league.pk) + ' | '+ str(self.team1) + ' vs. ' + str(self.team2)

class Upvote(models.Model):
  # Upvotes from another user - compliments for certain athletic feats during a match such as scoring capabilities, blocking, etc.
  vote_type = models.CharField()
  voting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voting_user')
  receiving_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiving_user')

  def __str__(self):
    """ Stringified representation of a model instance """
    return '' + self.vote_type + ': ' + str(self.voting_user) + '-->' + str(self.receiving_user) 


