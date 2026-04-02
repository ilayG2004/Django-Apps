from .models import *
from rest_framework import serializers

class JokeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Joke
    fields = ['joke', 'contributor', 'timestamp']

class PictureSerializer(serializers.ModelSerializer):
  class Meta:
    model = Picture
    fields = ['image_url', 'contributor', 'timestamp']