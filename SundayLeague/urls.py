from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views 

urlpatterns = [
  path('', ListLeagues.as_view(),name='home'),
  path('leagues/', ListLeagues.as_view(),name='list_leagues'),
  path('league/<int:pk>', DetailLeague.as_view(), name='detail_league'),
  path('team/<int:pk>', TeamDetail.as_view(), name='detail_team'),
  path('profile/<int:pk>', ProfileDetail.as_view(), name='detail_profile'),
  path('teams/', ListTeams.as_view(), name='list_teams'),

  #Not fully functional user views yet
  path('login/', CustomLoginView.as_view(), name='login'),
  path('logout/', auth_views.LogoutView.as_view(next_page='list_leagues'),name='logout'),
  path('my_leagues', MyLeagues.as_view(), name='my_leagues'),
  path('my_teams', MyTeams.as_view(), name='my_teams'),
  path('my_games', MyGames.as_view(), name='my_games'),

  path('create_league', CreateLeague.as_view(), name='create_league'),
  path('create_game/<int:pk>', CreateGame.as_view(), name='create_game'),
  path('create_team', CreateTeam.as_view(), name='create_team'),
  path('join_team/<int:pk>', CreateTeamJoinRequest.as_view(), name='join_team'),
  #path('create_team', CreateTeam.as_view(), name='create_team'),
  #path('create_team_join_request', CreateTeamJoinRequest.as_view(), name='create_team_join_request'),
  #path('create_league_join_request', CreateLeagueJoinRequest.as_view(), name='create_league_join_request')
]