# File: mini_insta/views.py
# Author: Ilay Guler (ilay2004@bu.edu), 2/12/2026
# Description: Using ListView and DetailView to render html templates using database model objects

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile


# Create your views here.
class ProfileListView(ListView):
  """ Uses show_all_profiles.html with ListView and the Profile model to display all profiles """
  model=Profile
  template_name="mini_insta/show_all_profiles.html"
  context_object_name="profiles"

class ProfileDetailView(DetailView):
  """ Uses show_profile.html with DetailView and the Profile model to show a single profile """
  model=Profile
  template_name="mini_insta/show_profile.html"
  context_object_name="profile"