# File: dadjokes/urls.py
# Author: Ilay Guler (ilay2004@bu.edu), 4/3/2026
# Description: Handles URL paths for normal dadjokes webapp as well as its REST API's

from django.urls import path, include
from django.contrib.auth import views as auth_views   
from .views import * # our view class definition 
from . import views
 
urlpatterns = [
  
  # Regular views:
  path(r'', views.random_view, name='home'),
  path(r'random', views.random_view, name='random'),
  path(r'jokes', ListJokeView.as_view(), name='joke_list'),
  path(r'joke/<int:pk>', DetailJokeView.as_view(), name='joke_detail'),
  path(r'pictures', ListPictureView.as_view(), name='pic_list'),
  path(r'picture/<int:pk>', DetailPictureView.as_view(), name='pic_detail'),

  # API views:   
  path(r'', RandomJokeAPI.as_view()),
  path(r'api/random', RandomJokeAPI.as_view()),
  path(r'api/jokes', ListJokesAPI.as_view()),
  path(r'api/joke/<int:pk>', DetailJokeAPI.as_view()),
  path(r'api/pictures', ListPicturesAPI.as_view()),
  path(r'api/picture/<int:pk>', DetailPictureAPI.as_view()),
  path(r'api/random_picture', RandomPictureAPI.as_view()),
]