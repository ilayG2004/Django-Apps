"""
FILE: SundayLeague/views.py
AUTHOR: Ilay Guler (ilay2004@bu.edu)
DESCRIPTION: Generic views and forms acting dynamically rendering content to users from html template by reading existing data model instances.
DATE: 4/17/2026
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.db.models import Q, Count, F
from django.db import transaction
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponse
from django.utils import timezone
from django.contrib import messages


def is_in_league(user, league):
  is_member = False
  if user.is_authenticated:
    teams = Team.objects.filter(teammember__user=user)
    for team in teams:
      if team.leagues.filter(pk=league.pk).exists():
        is_member=True
        break
  return is_member


# ------------- Genric Views ----------------

class ListLeagues(ListView):
  """ View to list active leagues """
  model=League
  template_name='SundayLeague/list_leagues.html'
  context_object_name='leagues'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context['sport_choices'] = League.SPORT_CHOICES

    return context
  
  def get_queryset(self):
    queryset = super().get_queryset()

    sport = self.request.GET.get('sport')
    level = self.request.GET.get('level')
    start_date = self.request.GET.get('start_date')
    end_date = self.request.GET.get('end_date')
    league_name = self.request.GET.get('name')

    queryset = queryset.filter(is_discoverable = True)
    
    # Check if number of teams associated with a league is not over the limit
    queryset = queryset.annotate(team_count=Count('teams'))
    queryset = queryset.filter(team_count__lt=F('max_teams'))

    if sport:
      queryset = queryset.filter(sport_type=sport)

    if level:
      queryset = queryset.filter(level__icontains=level)

    if start_date:
      queryset = queryset.filter(season_start__gte=start_date)
    
    if end_date:
      queryset = queryset.filter(season_end__lte=end_date)

    if league_name:
      queryset = queryset.filter(league_name__icontains=league_name)
    return queryset

class DetailLeague(DetailView):
  """ View to display league details """
  model=League
  template_name='SundayLeague/detail_league.html'
  context_object_name='league'

  def get_context_data(self, **kwargs):
    league = League.objects.get(pk=self.kwargs['pk'])

    user = self.request.user

    is_member = False
    is_some_team_admin = False

    if user.is_authenticated:
        is_member = is_in_league(user, league)
        is_some_team_admin = Team.objects.filter(team_admin=user).exists()

    games = league.getGames()
    upcoming_games = games.exclude(winner__isnull=False)
    completed_games = games.exclude(winner__isnull=True)

    return {
        "league": league,
        "upcoming_games": upcoming_games,
        "completed_games": completed_games,
        "teams": league.getTeams(),
        "leaderboard": league.getLeaderboard(),
        "posts": league.getPosts(),
        "is_member": is_member,
        "is_some_team_admin": is_some_team_admin,
        "time": timezone.now()
    }

class TeamDetail(DetailView):
  """ View to display a team's detailed page """
  model=Team
  template_name='SundayLeague/detail_team.html'
  context_object_name='team'

  """
  1.Add some logic in models.py to Team to get every TeamMember object associated with a team.
  2. Then we call that function inside the html and for loop thru it

  3. Calculate the team's win/losses through looking at game objects where two teams verse each other. Look at the winner attribute. If they won +1 win, else +1 loss
  """

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    team = self.object  # already fetched by DetailView
    members = team.getTeamMembers()
    context["members"] = members
    context["record"] = team.getWinLosses()

    user = self.request.user
    context["is_member"] = (
        user.is_authenticated and 
        members.filter(user=user).exists()
    )

    return context

class GameDetail(DetailView):
  model=Game
  template_name='SundayLeague/detail_game'
  content_object_name='game'

  """
  Simply display the teams. The time. Who won who lost if applicable.
  Add some logic that if the time for the game passed, and there was no update on the winner or score, render a 'Finalize' button for users who are part of the team, to fill out and update the info
  Requires a GameEdit form
  """

class ProfileDetail(DetailView):
  """ View to list a profile """
  model=SLProfile
  template_name='SundayLeague/detail_profile.html'
  content_object_name='profile'

  """Insert some logic:
  -Get all the teams they've ever been on
  -Collect all upvotes tied to this user (graphing can come at a way later update)
  """
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    profile = self.object
    context['profile'] = profile

    upvotes = (
        profile.getUpvotes()
        .values('vote_type')
        .annotate(count=Count('id'))
        .order_by()  # removes default ordering noise
    )
    # attach human-readable labels
    choice_map = dict(Upvote.UPVOTE_TYPES)
    for row in upvotes:
        row['label'] = choice_map[row['vote_type']]
    context["upvotes"] = upvotes


    context["teams"] = profile.getTeams()
    context['is_teammate'] = False
    if self.request.user.is_authenticated:
      viewing_profile = get_object_or_404(SLProfile, user=self.request.user)
      print("Viewing profile",viewing_profile)
      context['is_teammate'] = profile.isTeamMate(viewing_profile)
    return context
  
class ListTeams(ListView):
  """ View to list all active teams """
  model=Team
  template_name='SundayLeague/list_teams.html'
  context_object_name='teams'

  def get_queryset(self):
        queryset = super().get_queryset()

        team_name = self.request.GET.get('name')

        if team_name:
          queryset = queryset.filter(name__icontains=team_name)

        return queryset
  

# ------------- Login User Tabs -----------------
  
class MyTeams(LoginRequiredMixin, ListView):
  """ View to display teams for a user """
  login_url = 'login/'
  redirect_field_name = 'redirect_to'
  
  model = Team
  template_name = 'SundayLeague/my_pages/my_teams.html'
  context_object_name = 'teams'

  def get_queryset(self):
      profile = SLProfile.objects.get(user=self.request.user)
      queryset = profile.getTeams()

      team_name = self.request.GET.get('name')

      if team_name:
        queryset = queryset.filter(name__icontains=team_name)
      return queryset
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    teams = context['teams']
    context['managing'] = teams.filter(team_admin = self.request.user)
    return context
  
class MyLeagues(LoginRequiredMixin, ListView):
  """ View to display leagues for a user """
  login_url = 'login/'
  redirect_field_name = 'redirect_to'
  
  model = League
  template_name = 'SundayLeague/my_pages/my_leagues.html'
  context_object_name = 'leagues'

  def get_queryset(self):
    profile = SLProfile.objects.get(user=self.request.user)
    teams = profile.getTeams().values_list("id", flat=True)
    queryset = League.objects.filter(Q(teams__id__in=teams) |  Q(league_admin=self.request.user)).distinct()

    print("USER:", self.request.user)
    print("TEAMS:", teams)
    print("TEAM IDS:", list(teams.values_list("id", flat=True)))
    print("LEAGUES FOUND:", queryset)

    sport = self.request.GET.get('sport')
    level = self.request.GET.get('level')
    start_date = self.request.GET.get('start_date')
    end_date = self.request.GET.get('end_date')
    league_name = self.request.GET.get('name')

    if sport:
      queryset = queryset.filter(sport_type=sport)

    if level:
      queryset = queryset.filter(level__icontains=level)

    if start_date:
      queryset = queryset.filter(season_start__gte=start_date)
    
    if end_date:
      queryset = queryset.filter(season_end__lte=end_date)

    if league_name:
      queryset = queryset.filter(league_name__icontains=league_name)
    print("LEAGUES FINALIZED:", queryset)
    return queryset
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      leagues = context['leagues']
      now = timezone.localdate()
      context['managing'] = leagues.filter(league_admin = self.request.user)
      context['active'] = leagues.filter(season_start__lte=now, season_end__gte=now)
      context['previous'] = leagues.filter(season_end__lt=now)
      context['sport_choices'] = League.SPORT_CHOICES
      return context
    
    
class MyGames(LoginRequiredMixin, ListView):
    """ View to display games for a user """
    login_url = 'login/'
    redirect_field_name = 'redirect_to'
    
    model = Game
    template_name = 'SundayLeague/my_pages/my_games.html'
    context_object_name = 'games'

    def get_queryset(self):
        profile = SLProfile.objects.get(user=self.request.user)

        # Get user's teams (as queryset ideally)
        teams = profile.getTeams().values_list("id", flat=True)

        # Get all upcoming games involving those teams
        queryset = Game.objects.filter(
            Q(team1_id__in=teams) |
            Q(team2_id__in=teams)
        ).order_by('time')

        sport = self.request.GET.get('sport')
        level = self.request.GET.get('level')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        team_name = self.request.GET.get('name')

        if sport:
          queryset = queryset.filter(league__sport_type__icontains=sport)

        if level:
          queryset = queryset.filter(league__level__icontains=level)

        if start_date:
          queryset = queryset.filter(time__gte=start_date)
        
        if end_date:
          queryset = queryset.filter(time__lte=end_date)

        if team_name:
          queryset = queryset.filter(
              Q(team1__name__icontains=team_name) |
              Q(team2__name__icontains=team_name)
          )
        return queryset
    
    def get_context_data(self, **kwargs):
      """ Might be a little inefficient but we can worry about that later"""
      context = super().get_context_data(**kwargs)
       
      games = context['games']
      now = timezone.localdate()
      context['upcoming'] = games.filter(
        time__gt=now,
        winner__isnull=True
      )

      context['completed'] = games.filter(
          Q(time__lte=now) |
          Q(winner__isnull=False)
      )
      return context

# ---------- Custom Authentication Handling -----------

class CustomLoginView(LoginView):
  template_name = 'SundayLeague/login.html'

  def get_success_url(self):
      # If ?next= exists, respect it (important! for redirecting after a failed LoginRequiredMixin)
      next_url = self.request.GET.get('next')
      if next_url:
          return next_url

      # Otherwise redirect to user's profile
      profile = self.request.user.slprofile
      return reverse('detail_profile', kwargs={'pk': profile.pk})

def register(request):
  if request.method == "POST":
      form = UserRegisterForm(request.POST, request.FILES)

      if form.is_valid():
          with transaction.atomic():
              # Ensures both the django user and SLProfile are created safely
              user = form.save()

              SLProfile.objects.create(
                  user=user,
                  bio=form.cleaned_data.get('bio', ''),
                  profile_picture=form.cleaned_data.get('profile_picture')
              )

          login(request, user)
          return redirect("home")

  else:
      form = UserRegisterForm()

  return render(request, "SundayLeague/registration/register.html", {"form": form})

# ------ CREATE FORMS ------------
class CreateLeague(LoginRequiredMixin, CreateView):
  model=League
  form_class = CreateLeagueForm
  template_name = 'SundayLeague/create_forms/create_league.html'
  
  def form_valid(self, form):
      """ Assigns the league admin as the form creating user """
      form.instance.league_admin = self.request.user
      response = super().form_valid(form)
      messages.success(self.request, "League created successfully!")
      return response
  
  def get_success_url(self):
    return reverse('detail_league', kwargs={'pk': self.object.pk})

class CreateGame(LoginRequiredMixin, CreateView):
  model=Game
  form_class = CreateGameForm
  template_name='SundayLeague/create_forms/create_game.html'
  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     context['league'] = get_object_or_404(League, pk=self.kwargs['pk'])
     return context
  def get_form(self, form_class=None):
    """ Dropdown menu for team selection will only be teams in this league """
    form = super().get_form(form_class)

    league = get_object_or_404(League, pk=self.kwargs['pk'])

    teams_in_league = Team.objects.filter(leagues=league)

    form.fields['team1'].queryset = teams_in_league
    form.fields['team2'].queryset = teams_in_league
    
    return form

  def clean(self):
    """ Ensures team 1 neq team 2. And that they are still both part of the league (since the only other constraint would be a client-side form in get_form. Could still be tampered with.)"""
    cleaned_data = super().clean()

    team1 = cleaned_data.get("team1")
    team2 = cleaned_data.get("team2")

    league = self.initial.get("league")  # or pass via view

    if team1 and league and league not in team1.leagues.all():
        raise forms.ValidationError("Team 1 is not in this league.")

    if team2 and league and league not in team2.leagues.all():
        raise forms.ValidationError("Team 2 is not in this league.")

    if team1 and team2 and team1 == team2:
        raise forms.ValidationError("Teams must be different.")

    return cleaned_data
  
  def form_valid(self, form):
    """ Assigns the league to the game being created """
    league_pk = self.kwargs.get('pk')
    league = League.objects.get(pk=league_pk)
    if self.request.user != league.league_admin:
      return HttpResponse('Unauthorized', status=401)
    form.instance.league = league
    response = super().form_valid(form)
    return response
  
  def get_success_url(self):
    return reverse('detail_league', kwargs={'pk': self.kwargs.get('pk')})
  
class CreateTeam(LoginRequiredMixin, CreateView):
  model=Team
  form_class = CreateTeamForm
  template_name = 'SundayLeague/create_forms/create_team.html'

  def form_valid(self, form):
    """ Assigns the league admin as the form creating user """
    form.instance.team_admin = self.request.user
    
    response = super().form_valid(form)
    TeamMember.objects.create(
            user=self.request.user,
            team=self.object
        )
    messages.success(self.request, "Team created successfully!")
    return response
  
  def get_success_url(self):
    return reverse('detail_team', kwargs={'pk': self.object.pk})
  
class CreateTeamJoinRequest(LoginRequiredMixin, CreateView):
  model=TeamJoinRequest
  form_class = CreateTeamJoinRequestForm
  template_name = 'SundayLeague/create_forms/team_request.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    team = get_object_or_404(Team, pk=self.kwargs.get('pk'))
    context['team'] = team
    return context

  def form_valid(self, form):
    user = self.request.user
    team_pk = self.kwargs.get('pk')
    team = Team.objects.get(pk=team_pk)
    # Prevent duplicate request BEFORE saving
    if TeamJoinRequest.objects.filter(requesting_user=user, team=team).exists():
        messages.success(self.request, "Already requested to join this team. Request pending.")
        return redirect('detail_team', pk=team_pk)

    # Safe to create request
    form.instance.requesting_user = user
    form.instance.team = team

    response = super().form_valid(form)
    messages.success(self.request, "Join request sent!")
    return response

  def get_success_url(self):
    return reverse('detail_team', kwargs={'pk': self.kwargs.get('pk')})
  

class CreateTeamMember(LoginRequiredMixin, View):
  def post(self, request, team_pk, user_to_join):
    team = get_object_or_404(Team, pk=team_pk)

    # Permission check
    if team.team_admin != request.user:
        return HttpResponseForbidden("Not allowed")

    user = get_object_or_404(User, pk=user_to_join)

    # Ensure join request exists
    join_request = TeamJoinRequest.objects.filter(
        team=team,
        requesting_user=user
    ).first()

    if not join_request:
        messages.error(request, "Join request does not exist.")
        return redirect('check_team_requests', pk=team.pk)

    # Prevent duplicates
    if TeamMember.objects.filter(team=team, user=user).exists():
        messages.warning(request, "User is already a member.")
        join_request.delete()
        return redirect('check_team_requests', pk=team.pk)

    # Create member
    TeamMember.objects.create(team=team, user=user)

    # Delete request
    join_request.delete()

    messages.success(request, "User added to team.")

    return redirect('check_team_requests', pk=team.pk)

class CreateLeagueJoinRequest(LoginRequiredMixin, CreateView):
  model=LeagueJoinRequest
  form_class = CreateLeagueJoinRequestForm
  template_name = 'SundayLeague/create_forms/league_request.html'

  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     league = get_object_or_404(League, pk=self.kwargs.get('pk'))
     context['league'] = league
     return context

  def get_form(self, form_class=None):
    """ Dropdown menu for team selection will only be teams this user is admin of """
    form = super().get_form(form_class)
    managing_teams = Team.objects.filter(team_admin=self.request.user)
    form.fields['requesting_team'].queryset = managing_teams
    return form


  def form_valid(self, form):
    league = get_object_or_404(League, pk=self.kwargs.get('pk'))
    team = form.cleaned_data['requesting_team']

    # SECURITY: ensure user actually owns this team
    if team.team_admin != self.request.user:
        return HttpResponseForbidden("You do not control this team.")

    # Prevent duplicate requests
    if LeagueJoinRequest.objects.filter(requesting_team=team, league=league).exists():
        messages.warning(self.request, "Request already exists.")
        return redirect('detail_league', pk=league.pk)

    form.instance.league = league

    messages.success(self.request, "Join request sent!")
    return super().form_valid(form)

  def get_success_url(self):
    return reverse('detail_league', kwargs={'pk': self.kwargs.get('pk')})


class CreateLeagueMember(LoginRequiredMixin, View):
   def post(self, request, league_pk, team_to_join):
    league = get_object_or_404(League, pk=league_pk)

    # Permission check
    if league.league_admin != request.user:
        return HttpResponseForbidden("Not allowed")

    team = get_object_or_404(Team, pk=team_to_join)

    # Ensure join request exists
    join_request = LeagueJoinRequest.objects.filter(
        league=league,
        requesting_team=team
    ).first()

    if not join_request:
        messages.error(request, "Join request does not exist.")
        return redirect('check_league_requests', pk=league.pk)

    # Prevent duplicates
    if league in team.leagues.all():
        messages.warning(request, "Team is already in this league.")
        join_request.delete()
        return redirect('check_league_requests', pk=league.pk)

    # Enforce max teams constraint for a league
    if league.teams.count() >= league.max_teams:
        messages.error(request, "League is already full.")
        return redirect('check_league_requests', pk=league.pk)
    
    # Constraints satisfied. Add team to league
    team.leagues.add(league)

    # Delete request
    join_request.delete()

    messages.success(request, "Team successfully added to league")

    return redirect('check_league_requests', pk=league.pk)
   
class CreateLeaguePost(LoginRequiredMixin, CreateView):
   model=LeaguePost
   form_class=CreateLeaguePostForm
   template_name = 'SundayLeague/create_forms/create_league_post.html'
   
   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    league = get_object_or_404(League, pk=self.kwargs.get('pk'))
    context['league'] = league
    return context

   def dispatch(self, request, *args, **kwargs):
    """Security to make sure a user who enters the link is actually part of the league they're posting to"""
    league = get_object_or_404(League, pk=self.kwargs['pk'])

    # Get user's teams
    teams = Team.objects.filter(teammember__user=request.user)

    # Check membership
    is_member = teams.filter(leagues=league).exists()

    if not is_member:
        return HttpResponseForbidden("You are not a member of this league.")

    self.league = league  # store for later use
    return super().dispatch(request, *args, **kwargs)

   def form_valid(self, form):
    """ Assigns the posting user as the form's requesting user """
    form.instance.posting_user = self.request.user
    league = get_object_or_404(League, pk=self.kwargs['pk'])
    form.instance.league = league
    response = super().form_valid(form)
    messages.success(self.request, "Posted!")
    return response
   
   def get_success_url(self):
      return reverse('detail_league', kwargs={'pk': self.object.league.pk})

class CreateUpvote(LoginRequiredMixin, CreateView):
    """ Creates an upvote from one user to their teammate """
    model = Upvote
    form_class = CreateUpvoteForm
    template_name = 'SundayLeague/create_forms/create_upvote.html'

    def dispatch(self, request, *args, **kwargs):
      """ Ensures a user is not trying to vote for another user who is not on a team with them """
      voting_user = request.user
      receiving_profile = get_object_or_404(SLProfile, pk=kwargs['pk'])
    
      voting_profile = get_object_or_404(SLProfile, user=voting_user)
      print("VOTING USER:", voting_profile)
      print("RECEIVING USER:", receiving_profile)
      # Prevent self-voting (you probably want this)
      if voting_profile == receiving_profile:
          return HttpResponseForbidden("You cannot upvote yourself.")

      # Teammate check
      if not voting_profile.isTeamMate(receiving_profile):
          return HttpResponseForbidden("You can only upvote your teammates.")

      return super().dispatch(request, *args, **kwargs)

    def get_receiving_user(self):
      # assuming URL like: path('upvote/<int:pk>/...', ...)
      receiving_profile = SLProfile.objects.get(pk=self.kwargs['pk'])
      return receiving_profile.user

    def form_valid(self, form):
      voting_user = self.request.user
      receiving_user = self.get_receiving_user()

      # Delete existing upvote if it exists
      Upvote.objects.filter(
          voting_user=voting_user,
          receiving_user=receiving_user
      ).delete()

      # Assign users to the new upvote
      form.instance.voting_user = voting_user
      form.instance.receiving_user = receiving_user

      return super().form_valid(form)

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      profile = get_object_or_404(SLProfile, pk=self.kwargs.get('pk'))
      context['profile'] = profile
      return context

    def get_success_url(self):
      # Redirect back to receiving user's profile
      return reverse('detail_profile', kwargs={'pk': self.kwargs['pk']})
    

# ------------- DELETE VIEWS ----------------------
  
class DeleteTeamRequest(LoginRequiredMixin, View):
  def post(self, request, team_pk, user_to_join):
    team = get_object_or_404(Team, pk=team_pk)

    # Permission check
    if team.team_admin != request.user:
        return HttpResponseForbidden("Not allowed")

    user = get_object_or_404(User, pk=user_to_join)

    # Ensure join request exists
    join_request = TeamJoinRequest.objects.filter(
        team=team,
        requesting_user=user
    ).first()

    if not join_request:
        messages.error(request, "Join request does not exist.")
        return redirect('check_team_requests', pk=team.pk)

    # Delete request
    join_request.delete()

    messages.success(request, "Request ignored.")

    return redirect('check_team_requests', pk=team.pk)
  
class DeleteLeagueRequest(LoginRequiredMixin, View):
  def post(self, request, league_pk, team_to_join):
    league = get_object_or_404(League, pk=league_pk)

    # Permission check
    if league.league_admin != request.user:
        return HttpResponseForbidden("Not allowed")

    print("About to query team")
    team = get_object_or_404(Team, pk=team_to_join)

    # Ensure join request exists
    join_request = LeagueJoinRequest.objects.filter(
        league=league,
        requesting_team=team
    ).first()

    if not join_request:
        messages.error(request, "Join request does not exist.")
        return redirect('check_league_requests', pk=league.pk)

    # Delete request
    join_request.delete()

    messages.success(request, "Request ignored.")

    return redirect('check_league_requests', pk=league.pk)


class DeleteGame(LoginRequiredMixin, DeleteView):
   model = Game
   template_name='SundayLeague/delete_forms/delete_game.html'
   
   def dispatch(self, request, *args, **kwargs):
    game = self.get_object()

    if game.league.league_admin != request.user:
        return HttpResponseForbidden("You are not allowed to delete this game.")

    return super().dispatch(request, *args, **kwargs)
   
   def get_success_url(self):
    return reverse('detail_league', kwargs={'pk': self.object.league.pk})


class KickMembersView(LoginRequiredMixin, View):
    template_name = 'SundayLeague/delete_forms/kick_members.html'

    def get(self, request, pk):
        team = get_object_or_404(Team, pk=pk)

        # Permission check
        if team.team_admin != request.user:
            return HttpResponseForbidden("Not allowed.")

        members = TeamMember.objects.filter(team=team).exclude(
          user=team.team_admin
        ).select_related('user')

        return render(request, self.template_name, {
            'team': team,
            'members': members
        })

    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)

        # Permission check (again for POST)
        if team.team_admin != request.user:
            return HttpResponseForbidden("Not allowed.")

        member_ids = request.POST.getlist('members')

        # Only allow deleting members and NEVER the admin
        members_to_delete = TeamMember.objects.filter(
            team=team,
            id__in=member_ids
        ).exclude(user=team.team_admin)

        deleted_count = members_to_delete.count()
        members_to_delete.delete()
        messages.success(request, f"{deleted_count} member(s) removed.")

        return redirect('detail_team', pk=team.pk)


class KickTeams(LoginRequiredMixin, View):
   template_name = 'SundayLeague/delete_forms/kick_teams.html'
   
   def get(self, request, pk):
      league = get_object_or_404(League, pk=pk)

      if league.league_admin != request.user:
          return HttpResponseForbidden("Not allowed.")
      teams = Team.objects.filter(leagues=league)

      return render(request, self.template_name, {
          'league': league,
          'teams': teams
      })
   
   def post(self, request, pk):
      league = get_object_or_404(League, pk=pk)

      # Permission check (again for POST)
      if league.league_admin != request.user:
          return HttpResponseForbidden("Not allowed.")

      team_ids = request.POST.getlist('teams')
      teams = Team.objects.filter(
          id__in=team_ids,
          leagues=league
      )

      removed_count = 0
      for team in teams:
          team.leagues.remove(league)
          removed_count += 1

      messages.success(request, f"{removed_count} team(s) removed.")
      return redirect('detail_league', pk=league.pk)

# ---------- EDIT FORMS ------------------
class EditTeam(LoginRequiredMixin, UpdateView):
  model = Team
  form_class = UpdateTeamForm
  template_name = 'SundayLeague/update_forms/update_team.html'

  def get_queryset(self):
        """ Prevents non-team admin users from accessing this form """
        """ This is because get_queryset is used by django to fetch the object the form is changing """
        return Team.objects.filter(team_admin=self.request.user)
  def get_success_url(self):
    return reverse('detail_team', kwargs={'pk': self.kwargs.get('pk')})


class CheckTeamRequests(LoginRequiredMixin, View):
  template_name = 'SundayLeague/update_forms/check_team_requests.html'

  def get(self, request, pk):
    team = get_object_or_404(Team, pk=pk)

    if team.team_admin != request.user:
        return HttpResponseForbidden("Only team admins can check requests from users to join their team.")
    
    requests = TeamJoinRequest.objects.filter(team=team).select_related('requesting_user')

    return render(request, self.template_name, {
        'team': team,
        'requests': requests
    })
  
class CheckLeagueRequests(LoginRequiredMixin, View):
   template_name = 'SundayLeague/update_forms/check_league_requests.html'

   def get(self, request, pk):
      league = get_object_or_404(League, pk=pk)

      if league.league_admin != request.user:
         return HttpResponseForbidden("Only league admins can check requests from teams to join their league.")
      requests = LeagueJoinRequest.objects.filter(league=league).select_related('requesting_team')

      return render(request, self.template_name, {
         'league': league,
         'requests': requests
      })

class FinalizeScore(LoginRequiredMixin, UpdateView):
   model=Game
   form_class = FinalizeScoreForm
   template_name = 'SundayLeague/update_forms/finalize_score.html'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      game = self.get_object()
      league = game.league
      context['game'] = game
      context['league'] = league
      return context
   
   def dispatch(self, request, *args, **kwargs):
    game = self.get_object()
    league = game.league

    # Ensure that an outside user is not trying to edit this game
    if not is_in_league(self.request.user, league):
        return HttpResponseForbidden("You are not allowed to edit this game.")

    return super().dispatch(request, *args, **kwargs)
   
   def get_form(self, form_class=None):
    """ Dropdown menu for team selection will only be teams playing this game """
    form = super().get_form(form_class)
    form.fields['winner'].queryset = Team.objects.filter(
        pk__in=[self.object.team1.pk, self.object.team2.pk]
    )
    return form

   def get_success_url(self):
    return reverse('detail_league', kwargs={'pk': self.object.league.pk})
   
class EditProfile(LoginRequiredMixin, UpdateView):
   model=SLProfile
   form_class=UpdateProfileForm
   template_name = 'SundayLeague/update_forms/update_profile.html'
   
   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    profile = self.get_object()
    context['profile'] = profile
    return context  

   def dispatch(self, request, *args, **kwargs):
    """ Ensure an outside user is not trying to access an edit profile form for not themselves """
    profile = self.get_object()

    if not self.request.user == profile.user:
        return HttpResponseForbidden("You are not allowed to edit this profile.")

    return super().dispatch(request, *args, **kwargs)
   

   def get_success_url(self):
    return reverse('detail_profile', kwargs={'pk': self.object.pk})