# File: voter_analytics/urls.py
# Author: Ilay Guler (ilay2004@bu.edu), 3/20/2026
# Description: Paths to route clients to the correct webpages based on the URLs entered
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
  path('', ListVoters.as_view(), name="voters"),
  path('voter/<int:pk>', DetailVoter.as_view(), name="voter"),
  path('graphs/', GraphsView.as_view(), name="graphs"),
]