# File: mini_insta/urls.py
# Author: Ilay Guler (ilay2004@bu.edu), 2/12/2026
# Description: Give the mini_insta app url paths to access the show_all_profiles ListView, and the show_profile DetailView

# Changes 2/19: Added create_post path which uses the CreatePostView CreateView generic. And show_post which uses the PostDetailView DetailView generic
# Changes 2/27: Added URLs for Following, Followers, Delete, Update, Search
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
  path('', ProfileListView.as_view(), name="show_all_profiles"),
  path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
  path('profile/', MyProfileView.as_view(), name="my_profile"),
  path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
  path('profile/feed', PostFeedListView.as_view(), name="show_feed"),

  path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
  path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),

  path('profile/search', SearchView.as_view() ,name="search"),

  path('profile/create_post', CreatePostView.as_view(), name="create_post"),
  path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),
  path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
  path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
  path('login/', auth_views.LoginView.as_view(template_name="mini_insta/login.html"),name='login'),
  path('logout_confirmation/', LogoutConfirmationView.as_view(), name='logout_confirmation'),
  path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
  path('register/', CreateProfileView.as_view(), name='register'),

  path('post/<int:pk>/like', CreateLikeView.as_view(), name="like_post"),
  path('post/<int:pk>/unlike', DeleteLikeView.as_view(), name="unlike_post"),
  path('profile/<int:pk>/follow', CreateFollowView.as_view(), name="follow"),
  path('profile/<int:pk>/delete_follow', DeleteFollowView.as_view(), name="unfollow"),


  # REST APIs
  #Reading a profile or a list of profiles.
  path('api/read_profiles', ReadProfilesAPI.as_view()),
  path('api/read_feed/<int:pk>', ReadFeedAPI.as_view()),
  path('api/read_profile/<int:pk>', ReadProfileDetailAPI.as_view()),
  path('api/read_posts/<int:pk>', ReadPostsAPI.as_view()),
  path('api/create_post', CreatePostAPI.as_view()),
]