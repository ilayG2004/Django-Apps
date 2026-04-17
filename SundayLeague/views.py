"""
FILE: SundayLeague/views.py
AUTHOR: Ilay Guler (ilay2004@bu.edu)
DESCRIPTION: Generic views and forms acting dynamically rendering content to users from html template by reading existing data model instances.
DATE: 4/17/2026
"""
from django.shortcuts import render
from django.views.generic import *
from .models import *
# Create your views here.
class ListLeagues(ListView):
  model=League
  template_name='SundayLeague/list_leagues'
  context_object_name='leagues'