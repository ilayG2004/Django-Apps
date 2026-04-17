"""
FILE: SundayLeague/models.py
AUTHOR: Ilay Guler (ilay2004@bu.edu)
DESCRIPTION: Relational data models which are the backbone of interaction and data-exchange for this webapp
DATE: 4/17/2026
"""

from django.db import models
from django.contrib.auth.models import User
import datetime

class SLProfile(models.Model):
  # Customizable athelte profile attached to an authenticated User. Ideally I would have overriden regular User auth with an abstract user, but I did not want to
  # mess with the other apps in this project which user regular user auth.
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField
  profile_picture = models.ImageField()

class League(models.Model):
  # League is the grouping of teams for a sports league
  league_admin = models.ForeignKey(User, on_delete=models.CASCADE) # Controls league settings and can admit teams
  sport_type = models.CharField(blank=False)
  is_active = models.BooleanField(default=True)
  league_name = models.TextField(blank=False, default='Unnamed League')
  season_start = models.DateField()
  season_end = models.DateField()
  level = models.CharField(blank=False)

  def __str__(self):
    """ Stringified representation of a model instance """
    return ''+self.league_name + '-' +self.sport_type

class LeaguePost(models.Model):
  # Users on a team in a league can post messages to a board. 
  league = models.ForeignKey(League, on_delete=models.CASCADE)
  message = models.TextField()
  image = models.ImageField()
  posting_user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    """ Stringified representation of a model instance """
    return ''+self.league + '-' +self.posting_user + self.pk

class Team(models.Model):
  # A team is a grouping of users playing in a sport league
  team_admin = models.ForeignKey(User, on_delete=models.CASCADE) # Controls team settings and can add new members
  name = models.TextField()
  league = models.ForeignKey(League, on_delete=models.CASCADE)

  def __str__(self):
    """ Stringified representation of a model instance """
    return 'Team:'+self.league + '-' +self.name

class TeamMember(models.Model):
  # Connects an authenticated user to a team
  team = models.ForeignKey(Team, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    """ Stringified representation of a model instance """
    return 'Member: '+self.user + ' on ' +self.team


class Game(models.Model):
  # Connects two teams in a league, to a game scheduled at a certain time. Winner and final score are filled out when the match finishes
  league = models.ForeignKey(League, on_delete=models.CASCADE)
  time = models.DateField()
  team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_1')
  team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_2')
  winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winner')
  final_score = models.TextField(blank=True)
  location = models.TextField(blank=False, default='')

  def __str__(self):
    """ Stringified representation of a model instance """
    return '' + self.team1 + ' vs. ' + self.team2 + self.league.pk

class Upvote(models.Model):
  # Upvotes from another user - compliments for certain athletic feats during a match such as scoring capabilities, blocking, etc.
  vote_type = models.CharField()
  voting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voting_user')
  receiving_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiving_user')

  def __str__(self):
    """ Stringified representation of a model instance """
    return '' + self.vote_type + ': ' + self.voting_user + '-->' + self.receiving_user 


