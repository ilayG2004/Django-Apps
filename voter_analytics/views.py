# File: voter_analytics/views.py
# Author: Ilay Guler (ilay2004@bu.edu), 3/20/2026
# Description: Using ListView to display voter objects from our database with lots of voter objects
# DetailView to show individual voter object data
# Graph view to show deeper analysis across all voter objects

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView
from voter_analytics.models import *
from django.db.models import Min, Max, Count, Sum
from django.db.models.functions import ExtractYear
import plotly.express as px
from plotly.offline import plot

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

  def get_context_data(self, **kwargs):
      context= super().get_context_data(**kwargs)
      scores = [1, 2, 3, 4, 5]
      result = Voter.objects.aggregate(oldest_dob=Min("dob"),newest_dob=Max("dob"))
      oldest_year = result["oldest_dob"].year if result["oldest_dob"] else None
      newest_year = result["newest_dob"].year if result["newest_dob"] else None

      years = list(range(oldest_year,newest_year))
      context["years"] = years
      context["scores"] = scores
      return context

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

 
class DetailVoter(DetailView):
    """ Used to show DetailView of fields for a single Voter instance """
    model=Voter
    template_name="voter_analytics/voter_detail.html"
    context_object_name="voter"

class GraphsView(ListView):
    """ Utilizes ListView so that we can generate graphs based on querysets of Voter instances """
    model = Voter
    template_name = "voter_analytics/analytics.html"
    context_object_name = "voters"

    def get_queryset(self):
        """ Filtering queryset using the same logic from ListVoters"""
        # Yeah there's probably a more efficient way to do this than copying and pasting code. But you get the point
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

    def get_context_data(self, **kwargs):
        """ Returns div with html content of plotly charts inside to be displaye don html template """
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Histogram: Birth Year
        birth_data = (
            queryset.annotate(year=ExtractYear("dob"))
              .values("year")
              .annotate(count=Count("id"))
              .order_by("year")
        )

        years = [entry["year"] for entry in birth_data]
        counts = [entry["count"] for entry in birth_data]

        fig1 = px.bar(x=years, y=counts,
                      labels={"x": "Year of Birth", "y": "Count"},
                      title="Voters by Birth Year")

        context["birth_year_graph"] = plot(fig1, output_type="div")

        # Pie Chart: Party Affiliation
        party_data = (
            queryset.values("party_afil")
              .annotate(count=Count("id"))
        )

        labels = [entry["party_afil"] for entry in party_data]
        values = [entry["count"] for entry in party_data]

        fig2 = px.pie(names=labels, values=values,
                      title="Party Affiliation Distribution")

        context["party_graph"] = plot(fig2, output_type="div")

        # Election Participation
        """ Doing an aggregate function over each possible election to get a count, then making a bargraph based on the label, and count for each label """
        election_counts = queryset.aggregate(
            v20state=Sum("v20state"),
            v21town=Sum("v21town"),
            v21primary=Sum("v21primary"),
            v22general=Sum("v22general"),
            v23town=Sum("v23town"),
        )

        elections = list(election_counts.keys())
        votes = list(election_counts.values())

        fig3 = px.bar(x=elections, y=votes,
                      labels={"x": "Election", "y": "Number of Voters"},
                      title="Voter Participation by Election")

        context["election_graph"] = plot(fig3, output_type="div")


        """ Reused logic from ListView to feed in years and elections to filter """
        scores = [1, 2, 3, 4, 5]
        result = Voter.objects.aggregate(oldest_dob=Min("dob"),newest_dob=Max("dob"))
        oldest_year = result["oldest_dob"].year if result["oldest_dob"] else None
        newest_year = result["newest_dob"].year if result["newest_dob"] else None

        years = list(range(oldest_year,newest_year))
        context["years"] = years
        context["scores"] = scores
        context["visuals"] = True
        return context