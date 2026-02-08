from django.db import models

# Create your models here.
class Profile(models.Model):
  """Profile encompases basic data"""
  display_name = models.TextField(blank=True)
  username = models.TextField(blank=True, primary_key=True)
  profile_image_url = models.URLField(blank=True)
  bio_text = models.TextField(blank=True)
  join_date = models.DateField(auto_now=True)

  def __str__(self):
    """ To string of profile object. """
    return self.username