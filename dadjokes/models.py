# File: dadjokes/models.py
# Author: Ilay Guler (ilay2004@bu.edu), 4/3/2026
# Description: Setting up model for our Django app's db. This models.py defines the Joke & Picture model for our dadjokes app

from django.db import models

# Create your models here.

class Joke(models.Model):
  # Holds joke information
  joke = models.TextField(blank=True)
  contributor = models.TextField(blank=True)
  timestamp = models.DateField(auto_now=True)

class Picture(models.Model):
  # Holds picture information (no tassociated with jokes)
  image_url = models.URLField(blank=True)
  contributor = models.TextField(blank=True)
  timestamp = models.DateField(auto_now=True)

