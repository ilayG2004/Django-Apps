# File: mini_insta/urls.py
# Author: Ilay Guler (ilay2004@bu.edu), 2/19/2026
# Description: Added a ModelForm to create a Post

# Changes 2/27: Removed image_url
from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
  """ A form to add a post for a profile. Utilizes Post fields such as caption, but also defines a URL field for image url which is used in views.CreatePostView. """
  class Meta:
    """  this form with the Post model in our database """
    model=Post
    fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
  """ Changes all Profile fields for a Profile instance except the username & join date """
  class Meta:
    model=Profile
    fields=['display_name','profile_image_url','bio_text']

class UpdatePostForm(forms.ModelForm):
  class Meta:
    model=Post
    fields=['caption']

class CreateProfileForm(forms.ModelForm):
  class Meta:
    model=Profile
    fields=['username', 'display_name', 'bio_text','profile_image_url']