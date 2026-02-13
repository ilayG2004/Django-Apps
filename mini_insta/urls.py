# File: mini_insta/urls.py
# Author: Ilay Guler (ilay2004@bu.edu), 2/12/2026
# Description: Give the mini_insta app url paths to access the show_all_profiles ListView, and the show_profile DetailView

from django.urls import path
from .views import ProfileListView, ProfileDetailView

urlpatterns = [
  path('', ProfileListView.as_view(), name="show_all_profiles"),
  path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile")
]