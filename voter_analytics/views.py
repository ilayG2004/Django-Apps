# File: voter_analytics/views.py
# Author: Ilay Guler (ilay2004@bu.edu), 3/20/2026
# Description: Using ListView to display voter objects from our database with lots of voter objects

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView
from voter_analytics.models import *

# Create your views here.
def fake_view(request):
  response_text = f'''
  <html>
  <h1>Hello world</h1>
  </html>
  '''
  return HttpRequest(response_text)

class ListVoters(ListView):
  """ List 100 voters objects at a time """
  model = Voter
  template_name = "voter_analytics/voter_list.html"
  context_object_name = "voters"
  paginate_by = 100

  def get_queryset(self):
      queryset = super().get_queryset()

      # GET params
      party = self.request.GET.get("party")
      min_year = self.request.GET.get("min_year")
      max_year = self.request.GET.get("max_year")
      voter_score = self.request.GET.get("voter_score")

      # Filters
      if party:
          queryset = queryset.filter(party_afil=party)

      if min_year:
          queryset = queryset.filter(dob__year__gte=min_year)

      if max_year:
          queryset = queryset.filter(dob__year__lte=max_year)

      if voter_score:
          queryset = queryset.filter(voter_score=voter_score)

      # Boolean filters (checkboxes)
      if self.request.GET.get("v20state"):
          queryset = queryset.filter(v20state=True)

      if self.request.GET.get("v21town"):
          queryset = queryset.filter(v21town=True)

      if self.request.GET.get("v21primary"):
          queryset = queryset.filter(v21primary=True)

      if self.request.GET.get("v22general"):
          queryset = queryset.filter(v22general=True)

      if self.request.GET.get("v23town"):
          queryset = queryset.filter(v23town=True)

      return queryset

 
