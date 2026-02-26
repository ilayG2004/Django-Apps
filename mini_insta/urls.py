# File: mini_insta/urls.py
# Author: Ilay Guler (ilay2004@bu.edu), 2/12/2026
# Description: Give the mini_insta app url paths to access the show_all_profiles ListView, and the show_profile DetailView

# Changes 2/19: Added create_post path which uses the CreatePostView CreateView generic. And show_post which uses the PostDetailView DetailView generic
from django.urls import path
from .views import *

urlpatterns = [
  path('', ProfileListView.as_view(), name="show_all_profiles"),
  path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
  path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),

  path('profile/<int:pk>/feed', PostFeedListView.as_view(), name="show_feed"),

  path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
  path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),



  path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
  path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),
  path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
  path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
]