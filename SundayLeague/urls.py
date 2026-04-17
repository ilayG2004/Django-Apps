from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('',ListLeagues.as_view(),name='home')
]