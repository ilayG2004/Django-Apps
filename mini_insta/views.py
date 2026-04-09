# File: mini_insta/views.py
# Author: Ilay Guler (ilay2004@bu.edu), 2/12/2026
# Description: Using ListView and DetailView to render html templates using database model objects

# Changes 2/19: Added PostDetailView to show a DetailView for a single Post object. 
# And CreatePostView which handles the GET of a create_post_form.html to load a HTML form and the creation of a new Post and Photo object when the form is submitted.\

# Changes 2/27: Added the views for Followers, Following, Feed, Search
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Post, Photo
from .forms import *
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseNotFound
from rest_framework import generics
from .serializers import *



# ---------- REST API VIEWS -------------
class ReadProfilesAPI(generics.ListCreateAPIView):
   """ Return a JSON list of serialized profiles """
   queryset = Profile.objects.all()
   serializer_class=ProfileSerializer

class ReadProfileDetailAPI(generics.RetrieveAPIView): 
   """ Get a JSON of an individual profile """
   queryset = Profile.objects.all()
   serializer_class = ProfileSerializer

class ReadPostsAPI(generics.ListAPIView):
    """ Gets the posts and photos for each post for this profile """
    serializer_class = PostSerializer
    def get_queryset(self):
        # Default would be Post.objects.all() which would get all posts. 
        # We want just the posts for this profile, so filter by the url's pk
        qset = Post.objects.filter(profile=self.kwargs['pk'])
        return qset

class CreatePostAPI(generics.CreateAPIView):
   """ Create a post via rest api POST request """
   queryset = Post.objects.all()
   serializer_class = PostSerializer

class ReadFeedAPI(generics.RetrieveAPIView):
   """ Call the feed serializer which essentially runs the get_feed_posts method from the Profile model, but serialized """
   queryset=Profile.objects.all()
   serializer_class = FeedSerializer

# ---------- REGULAR DJANGO VIEWS -------------
class ProfileListView(ListView):
  """ Uses show_all_profiles.html with ListView and the Profile model to display all profiles """
  model=Profile
  template_name="mini_insta/show_all_profiles.html"
  context_object_name="profiles"

class MyProfileView(DetailView):
  model=Profile
  template_name="mini_insta/show_profile.html"
  context_object_name="profile"

  def get_object(self):
        return Profile.objects.get(user=self.request.user)

class ProfileDetailView(DetailView):
  """ Uses show_profile.html with DetailView and the Profile model to show a single profile """
  model=Profile
  template_name="mini_insta/show_profile.html"
  context_object_name="profile"

  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     if self.request.user.is_authenticated:
        context['requester_profile'] = Profile.objects.get(user=self.request.user)
     return context

class PostDetailView(DetailView):
  """ Uses show_post.html with DetailView and the Post model to show a single post """
  model= Post
  template_name="mini_insta/show_post.html"
  context_object_name="post"

  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     print(kwargs.items)
     if self.request.user.is_authenticated:
      profile=Profile.objects.get(user=self.request.user)
      context['liked'] = Like.objects.filter(profile=profile, post=self.object)
     return context

class CreatePostView(CreateView, LoginRequiredMixin):
  """ A view to create a Post for a Profile """
  """ Uses CreatePostForm to generate a form, and dynamically populate create_post_form.html """
  form_class = CreatePostForm
  template_name = "mini_insta/create_post_form.html"
  context_object_name = "profile"

  def get_success_url(self):
    """ Redirects us to the profile page after a new post is made for it """
    #self.kwargs is a dictionary containing URL parameters
    return reverse('my_profile')
  
  def form_valid(self, form):
    """ Handles form submission & saves new object to DB """
    """ We manually add the foriegn key (of Profile) to the Post object. And instantiate a new Photo object with its fkey as this Post"""
    profile = Profile.objects.get(user=self.request.user)
    form.instance.profile = profile
    post = form.save(commit=False)
    post.save()
    """
    #Read the image url from request.POS
    img_url = self.request.POST['files']
    if img_url:
        Photo.objects.create(post=post, image_url=img_url)
    """

    #Read the files
    #self.request.POST is text fields only, while self.request.FILES contains files
    img_files = self.request.FILES.getlist('files')
    if len(img_files) > 0:
      for file in img_files:
        Photo.objects.create(post=post, image_file=file)
        

    self.object = post
    return super().form_valid(form)
  
  def get_context_data(self, **kwargs):
    """ Allows us to access the profile object being referred to in the CreateView """
    context = super().get_context_data(**kwargs)
    profile = Profile.objects.get(user=self.request.user)
    context['profile']=profile
    return context
  
  def get_login_url(self):
    """Return the URL for this app's login page"""
    return reverse('login')
  
class UpdateProfileView(UpdateView, LoginRequiredMixin):
  """ Used to update a Profile instance """
  model=Profile
  form_class=UpdateProfileForm
  template_name="mini_insta/update_profile_form.html"
  context_object_name="profile"
  def get_object(self):
        return Profile.objects.get(user=self.request.user)
  
  def get_login_url(self):
     """Return the URL for this app's login page"""
     return reverse('login')
  
class CreateProfileView(CreateView):
   model=Profile
   form_class=CreateProfileForm
   template_name="mini_insta/create_profile_form.html"

   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['user_creation_form'] = UserCreationForm()
    return context
   
   def form_valid(self, form):
      """ Fetches the user creation form and saves the user object, which we then pass into the Profile instance """
      user_form = UserCreationForm(self.request.POST)

      if user_form.is_valid():
          user = user_form.save()

          login(self.request, user,
                backend='django.contrib.auth.backends.ModelBackend')

          form.instance.user = user
          return super().form_valid(form)

      return self.form_invalid(form)
      

class DeletePostView(DeleteView, LoginRequiredMixin):
  model=Post
  template_name = "mini_insta/delete_post_form.html"

  def get_context_data(self, **kwargs):
    """ Passes in the post & profile context variables to the HTML template"""
    context = super().get_context_data(**kwargs)
    context['post'] = self.object
    context['profile'] = self.object.profile
    return context
  
  def get_success_url(self, **kwargs):
    """ Goes back to the user profile after successful deletion """
    return self.object.profile.get_absolute_url()
  
  def get_login_url(self):
    """Return the URL for this app's login page"""
    return reverse('login')

class UpdatePostView(UpdateView, LoginRequiredMixin):
  """ Shows form to update a post """
  model=Post
  form_class=UpdatePostForm
  template_name="mini_insta/update_post_form.html"
  context_object_name = "post"

  def get_success_url(self):
    """ Redirects to the post page on submission """
    pk = self.kwargs['pk']
    return reverse('show_post', kwargs={'pk':pk})
  
  def get_login_url(self):
    """Return the URL for this app's login page"""
    return reverse('login')
  
  
class ShowFollowersDetailView(DetailView):
  """ Shows followers of a profile """
  model=Profile
  template_name="mini_insta/show_followers.html"
  context_object_name = "profile"

class ShowFollowingDetailView(DetailView):
  """ Shows following of a profile """
  model=Profile
  template_name="mini_insta/show_following.html"
  context_object_name = "profile"

class PostFeedListView(ListView, LoginRequiredMixin):
  model = Post
  template_name = "mini_insta/show_feed.html"
  context_object_name = "posts"

  def get_queryset(self):
      """ """
      profile = Profile.objects.get(user=self.request.user)
      return profile.get_post_feed()

  def get_context_data(self, **kwargs):
      """ """
      context = super().get_context_data(**kwargs)
      context['profile'] = Profile.objects.get(user=self.request.user)
      return context
  
  def get_login_url(self):
    """Return the URL for this app's login page"""
    return reverse('login')
  
class SearchView(ListView, LoginRequiredMixin):
  template_name = "mini_insta/search_results.html"
  context_object_name = "posts"

  def dispatch(self, request, *args, **kwargs):
      self.profile = Profile.objects.get(user=self.request.user)
      self.query = request.GET.get('query')

      # If no query provided render normal search form
      if not self.query:
          return render(
              request,
              "mini_insta/search.html",
              {"profile": self.profile}
          )

      # Otherwise continue normal ListView flow
      return super().dispatch(request, *args, **kwargs)

  def get_queryset(self):
      """ Queryset check non-case-sensitize caption contains query """
      # Return posts whose caption contains query text
      return Post.objects.filter(
          caption__icontains=self.query
      )

  def get_context_data(self, **kwargs):
      """ Query for posts with the captions, and profiles """
      context = super().get_context_data(**kwargs)

      # Add required context variables
      context['profile'] = self.profile
      context['query'] = self.query

      # Posts matching query (already available as object_list)
      context['posts'] = self.get_queryset()

      # Profiles matching query. Non case sensitive check text fields on profiles
      context['profiles'] = Profile.objects.filter(
          Q(username__icontains=self.query) |
          Q(display_name__icontains=self.query) |
          Q(bio_text__icontains=self.query)
      )

      return context
  
  def get_login_url(self):
    """Return the URL for this app's login page"""
    return reverse('login')

class LogoutConfirmationView(TemplateView):
    """ Redirect to display our logout page """
    template_name = "mini_insta/logged_out.html"


class CreateLikeView(TemplateView):
  """ Lets us save new likes to DB by getting the pk of the post and the requester profile """
  model=Like
   
  def dispatch(self, request, *args, **kwargs):
      liker_profile = Profile.objects.get(user=request.user)
      post = Post.objects.get(pk=kwargs['pk'])
      if Like.objects.filter(profile=liker_profile, post=post).exists():
         return HttpResponseNotFound("<h1>Post already liked</h1>")
      like_instance = Like(profile=liker_profile, post=post)
      like_instance.save()
      return redirect('show_post', pk=kwargs['pk'])

class DeleteLikeView(TemplateView):
  """ Lets us save delete likes on DB by getting the pk of the post and the requester profile """
  model=Like

  def dispatch(self, request, *args, **kwargs):
     like_remover_profile = Profile.objects.get(user=request.user)
     post = Post.objects.get(pk=kwargs['pk'])
     if not Like.objects.filter(profile=like_remover_profile, post=post).exists():
        return HttpResponseNotFound("<h1>Like object not found</h1>")
     like_instance = Like.objects.get(profile=like_remover_profile,post=post)
     like_instance.delete()
     return redirect('show_post',pk=kwargs['pk'])

class CreateFollowView(TemplateView):
  model = Follow

  def dispatch(self,request,*args,**kwargs):
     """ Creates a follow instance between the user requesting and the profile they clicked to follow """
     requester_profile = Profile.objects.get(user=request.user)
     profile_to_follow = Profile.objects.get(pk=kwargs['pk'])
     if Follow.objects.filter(profile=profile_to_follow, follower_profile=requester_profile).exists():
        """ Additional backend logic to prevent following twice (even if the follow button is not there) """
        return HttpResponseNotFound("<h1>Already follow this profile</h1>")
     
     if profile_to_follow != requester_profile:
        """ Create the follow instance and return back to the profile we were viewing """
        follow_instance = Follow(profile=profile_to_follow, follower_profile = requester_profile)
        follow_instance.save()
        return redirect('show_profile', pk=kwargs['pk'])
     else:
        return HttpResponseNotFound("<h1>No follow instance found between the request user's profile and the profile object selected.</h1>")
  
class DeleteFollowView(TemplateView):
  model=Follow

  def dispatch(self, request, *args, **kwargs):
     """ Removes a follow instance in the DB by identifying the profiles references and then finding the follow object in the DB """
     requester_profile = Profile.objects.get(user=self.request.user)
     following_profile = Profile.objects.get(pk = kwargs['pk'])
     follow_instance = Follow.objects.get(profile=following_profile, follower_profile=requester_profile)
     if follow_instance:
        follow_instance.delete()
        if 'following' in request.path:
          return redirect('show_following', pk=requester_profile.pk)
        else:
          return redirect('show_profile', pk=kwargs['pk'])
     else:
        return HttpResponseNotFound("<h1>No follow instance found between the request user's profile and the profile object selected.</h1>")
