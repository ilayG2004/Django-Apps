from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('', ListLeagues.as_view(),name='home'),
  path('league/<int:pk>', DetailLeague.as_view(), name='detail_league'),
  path('team/<int:pk>', TeamDetail.as_view(), name='detail_team'),
  path('profile/<int:pk>', ProfileDetail.as_view(), name='detail_profile'),
]