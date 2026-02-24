# File: mini_insta/views.py
# Author: Ilay Guler (ilay2004@bu.edu), 2/12/2026
# Description: Using ListView and DetailView to render html templates using database model objects

# Changes 2/19: Added PostDetailView to show a DetailView for a single Post object. 
# And CreatePostView which handles the GET of a create_post_form.html to load a HTML form and the creation of a new Post and Photo object when the form is submitted.
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm
from django.urls import reverse


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
  
  def get_context_data(self):
    """ Allows us to access the profile object being referred to in the CreateView """
    context = super().get_context_data()
    pk=self.kwargs['pk']
    profile = Profile.objects.get(pk=pk)
    context['profile']=profile
    return context
  
class UpdateProfileView(UpdateView):
  model=Profile
  form_class=UpdateProfileForm
  template_name="mini_insta/update_profile_form.html"
  context_object_name="profile"