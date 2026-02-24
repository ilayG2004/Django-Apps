# File: mini_insta/models.py
# Author: Ilay Guler (ilay2004@bu.edu), 2/12/2026
# Description: Setting up model for our Django app's db. This models.py defines the Profile model for our mini_insta app.

#Changes 2/19: Added Post and Photo models to database. Each with their own fields and toString method. Added get_absolute_url to the Profile model.
#Changes 2/27: Added image_file attribute to Photo model. Added an accessor method get_image_url which returns the URL of an image regardless of how it is stored (URL or file). Revised __str__ emthod for the Photo model

from django.db import models
from django.urls import reverse

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
  def get_all_posts(self):
    """ Return queryset of all Post instances whose profile attribute matches this Profile instance. Ordered by timestamp """
    posts = Post.objects.filter(profile=self).order_by('timestamp')
    return posts
  def get_absolute_url(self):
    """ Return the URL to display one instance of this model """
    return reverse('show_profile', kwargs={'pk': self.pk})

  
class Post(models.Model):
  """ Defines fields of a post, which has Profile as a foreign key. """
  """ Each profile can have many posts. """
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  timestamp = models.DateField(auto_now=True)
  caption = models.TextField(blank=True)

  def __str__(self):
    """ To string of Post object. """
    return f"Post {self.pk} by {self.profile.username}"
  
  def get_all_photos(self):
    """ Return queryset of all Post instances whose profile attribute matches this Profile instance. Ordered by timestamp """
    photos = Photo.objects.filter(post=self)
    return photos

class Photo(models.Model):
  """ Defines fields of a photo, which defines Post as a foreign key. """
  """ Each post can have many photos. """
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  image_url = models.URLField(blank=True)
  timestamp = models.DateField(auto_now=True)
  image_file = models.ImageField(blank=True)

  def get_image_url(self):
    """ Returns a URL corresponding to an image. Backwards compatible with our old way of storing image urls in the DB instead of files """
    if self.image_url:
      return self.image_url
    elif self.image_file:
      return self.image_file.url
    else:
      return ""
    
  def __str__(self):
    """ To string of Photo object. """
    return f"Photo {self.pk} for Post {self.post_id}"