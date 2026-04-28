"""
FILE: SundayLeague/urls.py
AUTHOR: Ilay Guler (ilay2004@bu.edu)
DESCRIPTION: URL paths for client to request resources from our app. Each URL maps to a view.
DATE: 4/17/2026
"""
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
  # Generic views
  path('', ListLeagues.as_view(),name='home'),
  path('leagues/', ListLeagues.as_view(),name='list_leagues'),
  path('league/<int:pk>', DetailLeague.as_view(), name='detail_league'),
  path('team/<int:pk>', TeamDetail.as_view(), name='detail_team'),
  path('profile/<int:pk>', ProfileDetail.as_view(), name='detail_profile'),
  path('teams/', ListTeams.as_view(), name='list_teams'),

  # Auth user views
  path('register/', views.register, name='register'),
  path('login/', CustomLoginView.as_view(), name='login'),
  path('logout/', auth_views.LogoutView.as_view(next_page='list_leagues'),name='logout'),
  path('my_leagues/', MyLeagues.as_view(), name='my_leagues'),
  path('my_teams/', MyTeams.as_view(), name='my_teams'),
  path('my_games/', MyGames.as_view(), name='my_games'),

  # User creation of league or teams
  path('create_league/', CreateLeague.as_view(), name='create_league'),
  path('create_team/', CreateTeam.as_view(), name='create_team'),

  path('join_team/<int:pk>/', CreateTeamJoinRequest.as_view(), name='join_team'),

  # Team admin management
  path('edit_team/<int:pk>/', EditTeam.as_view(), name='edit_team'),
  path('kick_members/<int:pk>/', KickMembersView.as_view(), name='kick_members'),
  path('create_league_request/<int:pk>/', CreateLeagueJoinRequest.as_view(), name='create_league_request'),

  # Team admin join requests
  path('check_team_requests/<int:pk>/', CheckTeamRequests.as_view(), name='check_team_requests'),
  path('add_member/<int:team_pk>/<int:user_to_join>/', CreateTeamMember.as_view(), name='create_member'),
  path('remove_request/<int:team_pk>/<int:user_to_join>/', DeleteTeamRequest.as_view(), name='delete_team_request'),

  # League admin management
  path('create_game/<int:pk>/', CreateGame.as_view(), name='create_game'),
  path('delete_game/<int:pk>/', DeleteGame.as_view(), name='delete_game'),
  path('finalize_score/<int:pk>/', FinalizeScore.as_view(), name='finalize_score'),
  path('kick_teams/<int:pk>/', KickTeams.as_view(), name='kick_teams'),

  # League admin join requests
  path('check_league_requests/<int:pk>/', CheckLeagueRequests.as_view(), name='check_league_requests'),
  path('team_join_league/<int:league_pk>/<int:team_to_join>/', CreateLeagueMember.as_view(), name='team_join_league'),
  path('remove_team_league_request/<int:league_pk>/<int:team_to_join>/', DeleteLeagueRequest.as_view(), name='delete_league_request'),

  # League member posts
  path('create_league_post/<int:pk>/', CreateLeaguePost.as_view(), name='create_league_post')

  #path('create_team', CreateTeam.as_view(), name='create_team'),
  #path('create_team_join_request', CreateTeamJoinRequest.as_view(), name='create_team_join_request'),
  #path('create_league_join_request', CreateLeagueJoinRequest.as_view(), name='create_league_join_request')
]