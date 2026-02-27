# File: mini_insta/views.py
# Author: Ilay Guler (ilay2004@bu.edu), 2/12/2026
# Description: Using ListView and DetailView to render html templates using database model objects

# Changes 2/19: Added PostDetailView to show a DetailView for a single Post object. 
# And CreatePostView which handles the GET of a create_post_form.html to load a HTML form and the creation of a new Post and Photo object when the form is submitted.\

# Changes 2/27: Added the views for Followers, Following, Feed, Search
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import *
from django.urls import reverse
from django.db.models import Q



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

class PostDetailView(DetailView):
  """ Uses show_post.html with DetailView and the Post model to show a single post """
  model= Post
  template_name="mini_insta/show_post.html"
  context_object_name="post"

class CreatePostView(CreateView):
  """ A view to create a Post for a Profile """
  """ Uses CreatePostForm to generate a form, and dynamically populate create_post_form.html """
  form_class = CreatePostForm
  template_name = "mini_insta/create_post_form.html"
  context_object_name = "profile"

  def get_success_url(self):
    """ Redirects us to the profile page after a new post is made for it """
    #self.kwargs is a dictionary containing URL parameters
    pk = self.kwargs['pk']
    return reverse('show_profile', kwargs={'pk':pk})
  
  def form_valid(self, form):
    """ Handles form submission & saves new object to DB """
    """ We manually add the foriegn key (of Profile) to the Post object. And instantiate a new Photo object with its fkey as this Post"""
    print(form.cleaned_data)

    #Attach pk from URL to profile attribute of Post
    pk = self.kwargs['pk']
    profile = Profile.objects.get(pk=pk)
    form.instance.profile=profile

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
    pk=self.kwargs['pk']
    profile = Profile.objects.get(pk=pk)
    context['profile']=profile
    return context
  
class UpdateProfileView(UpdateView):
  """ Used to update a Profile instance """
  model=Profile
  form_class=UpdateProfileForm
  template_name="mini_insta/update_profile_form.html"
  context_object_name="profile"

class DeletePostView(DeleteView):
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

class UpdatePostView(UpdateView):
  """ Shows form to update a post """
  model=Post
  form_class=UpdatePostForm
  template_name="mini_insta/update_post_form.html"
  context_object_name = "post"

  def get_success_url(self):
    """ Redirects to the post page on submission """
    pk = self.kwargs['pk']
    return reverse('show_post', kwargs={'pk':pk})
  
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

class PostFeedListView(ListView):
  model = Post
  template_name = "mini_insta/show_feed.html"
  context_object_name = "posts"

  def get_queryset(self):
      """ """
      profile = Profile.objects.get(pk=self.kwargs['pk'])
      return profile.get_post_feed()

  def get_context_data(self, **kwargs):
      """ """
      context = super().get_context_data(**kwargs)
      context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
      return context
  
class SearchView(ListView):
  template_name = "mini_insta/search_results.html"
  context_object_name = "posts"

  def dispatch(self, request, *args, **kwargs):
      self.profile = Profile.objects.get(pk=self.kwargs['pk'])
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
