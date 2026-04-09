# File: mini_insta/serializers.py
# Author: Ilay Guler (ilay2004@bu.edu), 4/7/2026
# Description: Handles serializing django model instance data into byte data to transmit in txt format as json's


from .models import *
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
  # Serializes a joke instance and all of its fields
  post_photos = serializers.SerializerMethodField()
  class Meta:
    model = Post
    fields = ['pk', 'profile', 'timestamp', 'caption', 'post_photos']

  def get_post_photos(self, obj):
    post_photos = obj.get_all_photos() 
    return PhotoSerializer(post_photos, many=True).data
  
  

class FeedSerializer(serializers.ModelSerializer):
  # Serializes a picture instance and all of its fields
  feed_posts = serializers.SerializerMethodField()
  class Meta:
    model = Profile
    fields = ['pk', 'user', 'display_name', 'username', 'profile_image_url', 'bio_text', 'join_date', 'feed_posts']

  # This should lowkey not be called every time we want a list of profiles or we will have an explosively large json
  def get_feed_posts(self, obj):
    posts = obj.get_post_feed()
    return PostSerializer(posts, many=True).data
  
class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['pk', 'user', 'display_name', 'username', 'profile_image_url', 'bio_text', 'join_date']


class PhotoSerializer(serializers.ModelSerializer):
  class Meta:
    model=Photo
    fields=['pk', 'post','image_url','timestamp','image_file']