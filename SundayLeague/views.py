"""
FILE: SundayLeague/views.py
AUTHOR: Ilay Guler (ilay2004@bu.edu)
DESCRIPTION: Generic views and forms acting dynamically rendering content to users from html template by reading existing data model instances.
DATE: 4/17/2026
"""
from django.shortcuts import render
from django.views.generic import *
from .models import *
# Create your views here.
class ListLeagues(ListView):
  model=League
  template_name='SundayLeague/list_leagues.html'
  context_object_name='leagues'

class DetailLeague(DetailView):
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
    context["upvotes"] = profile.getUpvotes()
    context["teams"] = profile.getTeams()
    return context