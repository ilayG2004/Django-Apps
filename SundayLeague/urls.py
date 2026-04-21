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
  path('logout/', CustomLogoutView.as_view(), name='logout'),
  path('my_leagues', DetailLeague.as_view(), name='my_leagues'),
  path('my_teams', DetailLeague.as_view(), name='my_teams'),
  path('my_games', DetailLeague.as_view(), name='my_games'),
]