# File: mini_insta/urls.py
# Author: Ilay Guler (ilay2004@bu.edu), 2/19/2026
# Description: Added a ModelForm to create a Post

from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
  """ A form to add a post for a profile. Utilizes Post fields such as caption, but also defines a URL field for image url which is used in views.CreatePostView. """
  image_url = forms.URLField(required=False)
  class Meta:
    """  this form with the Post model in our database """
    model=Post
    fields = ['caption']