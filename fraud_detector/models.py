from django.db import models

# Create your models here.
class Joke(models.Model):
  joke = models.TextField(blank=True)
  contributor = models.TextField(blank=True)
  timestamp = models.DateField(auto_now=True)

class Picture(models.Model):
  image_url = models.URLField(blank=True)
  contributor = models.TextField(blank=True)
  timestamp = models.DateField(auto_now=True)

