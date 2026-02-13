# File: mini_insta/models.py
# Author: Ilay Guler (ilay2004@bu.edu), 2/12/2026
# Description: Setting up model for our Django app's db. This models.py defines the Profile model for our mini_insta app.

from django.db import models

# Create your models here.
class Profile(models.Model):
  """ Defining fields of the Profile, corresponding to basic user data. These will be column in our table. """
  display_name = models.TextField(blank=True)
  username = models.TextField(blank=True)
  profile_image_url = models.URLField(blank=True)
  bio_text = models.TextField(blank=True)
  join_date = models.DateField(auto_now=True)

  def __str__(self):
    """ To string of profile object. """
    return self.username