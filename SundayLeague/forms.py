from django import forms
from .models import *


# ------------- Create Forms -----------------------

class CreateLeagueForm(forms.ModelForm):
  """ Form associated with creating a Team for a respective league """
  """ league_admin derived from requesting league creator """


  # Sets our date fields to actual calendar widgets
  season_start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

  season_end = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
  class Meta:
    model=League
    fields = ['sport_type','max_teams','league_name', 'season_start', 'season_end', 'level']

  def clean(self):
    """ Ensures an invalid league is not made """
    cleaned_data = super().clean()
    start = cleaned_data.get("season_start")
    end = cleaned_data.get("season_end")
    if start and end and end < start:
        raise forms.ValidationError("Season end must be after start.")

    level = cleaned_data.get("level")
    if level not in ["1", "2", "3"]:
      raise forms.ValidationError("Competition level should be either 1, 2, or 3.")
    
    return cleaned_data
  

class CreateGameForm(forms.ModelForm):
  """ Form associated with creating a game """
  """ league should be automatically derived automatically. Though I'm not sure how yet"""
  """ winner & final_score should be blank on creation, and filled out later by a league member """
  
  time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
  class Meta:
    model=Game
    fields = ['time', 'team1', 'team2', 'location']
  
class CreateLeaguePostForm(forms.ModelForm):
  """ Form associated with creating a post for a respective league """
  """ posting_user derived from authenticated user filling out this form. League derived from pk. """
  class Meta:
    model = LeaguePost
    fields = ['message', 'image']

class CreateTeamForm(forms.ModelForm):
  """ Form associated with creating a Team for a respective league """
  """ team_admin derived from requesting team creator """
  """ max_team members should be added so we can filter discovering this team """
  """ and also, joining an empty team to a league is kind of weird. We should allow a single team to exist indepdent of a league. And allow it to join many """
  class Meta:
    model=Team
    fields = ['name', 'picture','bio']

class CreateTeamJoinRequestForm(forms.ModelForm):
  """ Form associated with a user requesting to join a team. The team and user should be derived from the interaction """
  class Meta:
    model=TeamJoinRequest
    fields=['message']

class CreateLeagueJoinRequestForm(forms.ModelForm):
  class Meta:
    model=LeagueJoinRequest
    fields=['requesting_team', 'message']


# -------------- Update forms -----------
class UpdateTeamForm(forms.ModelForm):
  class Meta:
    model=Team
    fields=['name','picture','bio']

class FinalizeScoreForm(forms.ModelForm):
  """ Updates the details of who won a game """
  class Meta:
    model=Game
    fields=['winner', 'final_score']