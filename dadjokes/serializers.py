# File: dadjokes/serializers.py
# Author: Ilay Guler (ilay2004@bu.edu), 4/3/2026
# Description: Handles serializing django model instance data into byte data to transmit in txt format as json's


from .models import *
from rest_framework import serializers

class JokeSerializer(serializers.ModelSerializer):
  # Serializes a joke instance and all of its fields
  class Meta:
    model = Joke
    fields = ['joke', 'contributor', 'timestamp']

class PictureSerializer(serializers.ModelSerializer):
  # Serializes a picture instance and all of its fields
  class Meta:
    model = Picture
    fields = ['image_url', 'contributor', 'timestamp']