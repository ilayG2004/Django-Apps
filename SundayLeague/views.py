"""
FILE: SundayLeague/views.py
AUTHOR: Ilay Guler (ilay2004@bu.edu)
DESCRIPTION: Generic views and forms acting dynamically rendering content to users from html template by reading existing data model instances.
DATE: 4/17/2026
"""
from django.shortcuts import render
from django.views.generic import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest
from django.utils import timezone
# Create your views here.
class ListLeagues(ListView):
  """ View to list active leagues """
  model=League
  template_name='SundayLeague/list_leagues.html'
  context_object_name='leagues'

  def get_queryset(self):
    queryset = super().get_queryset()

    sport = self.request.GET.get('sport')
    level = self.request.GET.get('level')
    start_date = self.request.GET.get('start_date')
    end_date = self.request.GET.get('end_date')
    league_name = self.request.GET.get('name')

    if sport:
      queryset = queryset.filter(sport_type__icontains=sport)

    if level:
      queryset = queryset.filter(level__icontains=level)

    if start_date:
      queryset = queryset.filter(season_start__gte=start_date)
    
    if end_date:
      queryset = queryset.filter(season_end__lte=end_date)

    if league_name:
      queryset = queryset.filter(league_name__icontains=league_name)
    return queryset

class DetailLeague(DetailView):
  """ View to display league details """
  model=League
  template_name='SundayLeague/detail_league.html'
  context_object_name='league'

  """Insert some logic: 
  -Filter games in the league. Ordering by closest start date first
  -Get all teams in this league
  -Filter which team has the most wins right now. Which has the most losses
  -Get all league posts
  """

  def get_context_data(self, **kwargs):
    league = League.objects.get(pk=self.kwargs['pk'])
    context = {
        "league": league,
        "games": league.getGames(),
        "teams": league.getTeams(),
        "leaderboard": league.getLeaderboard(),
        "posts": league.getPosts(),
    }
    return context

class TeamDetail(DetailView):
  """ View to display a team's detailed page """
  model=Team
  template_name='SundayLeague/detail_team.html'
  context_object_name='team'

  """
  1.Add some logic in models.py to Team to get every TeamMember object associated with a team.
  2. Then we call that function inside the html and for loop thru it

  3. Calculate the team's win/losses through looking at game objects where two teams verse each other. Look at the winner attribute. If they won +1 win, else +1 loss
  """

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    team = self.object  # already fetched by DetailView

    context["members"] = team.getTeamMembers()
    context["record"] = team.getWinLosses()

    return context

class GameDetail(DetailView):
  model=Game
  template_name='SundayLeague/detail_game'
  content_object_name='game'

  """
  Simply display the teams. The time. Who won who lost if applicable.
  Add some logic that if the time for the game passed, and there was no update on the winner or score, render a 'Finalize' button for users who are part of the team, to fill out and update the info
  Requires a GameEdit form
  """

class ProfileDetail(DetailView):
  """ View to list a profile """
  model=SLProfile
  template_name='SundayLeague/detail_profile.html'
  content_object_name='profile'

  """Insert some logic:
  -Get all the teams they've ever been on
  -Collect all upvotes tied to this user (graphing can come at a way later update)
  """
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    profile = self.object
    context['profile'] = profile
    upvotes = profile.getUpvotes()
    aggregate = {}
    for upvote in upvotes:
      if upvote.vote_type not in aggregate:
        aggregate[upvote.vote_type] = 1
      else:
        aggregate[upvote.vote_type] += 1
    context["upvotes"] = aggregate
    context["teams"] = profile.getTeams()
    return context
  
class ListTeams(ListView):
  """ View to list all active teams """
  model=Team
  template_name='SundayLeague/list_teams.html'
  context_object_name='teams'

  def get_queryset(self):
        queryset = super().get_queryset()

        sport = self.request.GET.get('sport')
        level = self.request.GET.get('level')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        team_name = self.request.GET.get('name')

        if sport:
          queryset = queryset.filter(league__sport_type__icontains=sport)

        if level:
          queryset = queryset.filter(league__level__icontains=level)

        if start_date:
          queryset = queryset.filter(league__season_start__gte=start_date)
        
        if end_date:
          queryset = queryset.filter(league__season_end__lte=end_date)

        if team_name:
          queryset = queryset.filter(name__icontains=team_name)
        return queryset
  

"""---------- Log-in User Tabs -----------------"""
  
class MyTeams(LoginRequiredMixin, ListView):
  """ View to display teams for a user """
  login_url = 'login/'
  redirect_field_name = 'redirect_to'
  
  model = Team
  template_name = 'SundayLeague/my_pages/my_teams.html'
  context_object_name = 'teams'

  def get_queryset(self):
      profile = SLProfile.objects.get(user=self.request.user)
      queryset = profile.getTeams()

      sport = self.request.GET.get('sport')
      level = self.request.GET.get('level')
      start_date = self.request.GET.get('start_date')
      end_date = self.request.GET.get('end_date')
      team_name = self.request.GET.get('name')

      if sport:
        queryset = queryset.filter(league__sport_type__icontains=sport)

      if level:
        queryset = queryset.filter(league__level__icontains=level)

      if start_date:
        queryset = queryset.filter(league__season_start__gte=start_date)
      
      if end_date:
        queryset = queryset.filter(league__season_end__lte=end_date)

      if team_name:
        queryset = queryset.filter(name__icontains=team_name)
      return queryset
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      teams = context['teams']

      context['active'] = teams.filter(league__is_active=True)
      context['previous'] = teams.filter(league__is_active=False)
      return context
  
class MyLeagues(LoginRequiredMixin, ListView):
  """ View to display leagues for a user """
  login_url = 'login/'
  redirect_field_name = 'redirect_to'
  
  model = League
  template_name = 'SundayLeague/my_pages/my_leagues.html'
  context_object_name = 'leagues'

  def get_queryset(self):
    profile = SLProfile.objects.get(user=self.request.user)
    teams = profile.getTeams()
    queryset = League.objects.filter(team__in=teams).distinct()

    sport = self.request.GET.get('sport')
    level = self.request.GET.get('level')
    start_date = self.request.GET.get('start_date')
    end_date = self.request.GET.get('end_date')
    league_name = self.request.GET.get('name')

    if sport:
      queryset = queryset.filter(sport_type__icontains=sport)

    if level:
      queryset = queryset.filter(level__icontains=level)

    if start_date:
      queryset = queryset.filter(season_start__gte=start_date)
    
    if end_date:
      queryset = queryset.filter(season_end__lte=end_date)

    if league_name:
      queryset = queryset.filter(league_name__icontains=league_name)
    return queryset
  
  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     leagues = context['leagues']
     context['active'] = leagues.filter(is_active = True)
     context['previous'] = leagues.filter(is_active = False)

     return context
    
    
class MyGames(LoginRequiredMixin, ListView):
    """ View to display games for a user """
    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    
    model = Game
    template_name = 'SundayLeague/my_pages/my_games.html'
    context_object_name = 'games'

    def get_queryset(self):
        profile = SLProfile.objects.get(user=self.request.user)

        # Get user's teams (as queryset ideally)
        teams = profile.getTeams()

        # Get all upcoming games involving those teams
        queryset = Game.objects.filter(
            (Q(team1__in=teams) | Q(team2__in=teams)) &
            Q(winner=None)
        ).order_by('time')

        sport = self.request.GET.get('sport')
        level = self.request.GET.get('level')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        team_name = self.request.GET.get('name')

        if sport:
          queryset = queryset.filter(league__sport_type__icontains=sport)

        if level:
          queryset = queryset.filter(league__level__icontains=level)

        if start_date:
          queryset = queryset.filter(time__gte=start_date)
        
        if end_date:
          queryset = queryset.filter(time__lte=end_date)

        if team_name:
          queryset = queryset.filter(
              Q(team1__name__icontains=team_name) |
              Q(team2__name__icontains=team_name)
          )
        return queryset
    
    def get_context_data(self, **kwargs):
      """ Might be a little inefficient but we can worry about that later"""
      context = super().get_context_data(**kwargs)
       
      games = context['games']
      now = timezone.now()
      context['upcoming'] = games.filter(time__gt=now)
      context['completed'] = games.filter(time__lt=now)
      return context

class CustomLoginView(LoginView):
    template_name = 'SundayLeague/login.html'

    def get_success_url(self):
        # If ?next= exists, respect it (important!)
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url

        # Otherwise redirect to user's profile
        profile = self.request.user.slprofile
        return reverse('detail_profile', kwargs={'pk': profile.pk})