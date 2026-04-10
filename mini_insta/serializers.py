# File: mini_insta/serializers.py
# Author: Ilay Guler (ilay2004@bu.edu), 4/7/2026
# Description: Handles serializing django model instance data into byte data to transmit in txt format as json's


from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
  # Serializes a joke instance and all of its fields
  post_photos = serializers.SerializerMethodField()
  username = serializers.SerializerMethodField()
  class Meta:
    model = Post
    fields = ['pk', 'profile', 'timestamp', 'caption', 'post_photos', 'username']

  def get_post_photos(self, obj):
    post_photos = obj.get_all_photos() 
    return PhotoSerializer(post_photos, many=True).data
  
  def get_username(self, obj):
   # Fetch the full username based on the pk of the 'profile' field associated with a post
   # Possibly redundant, but this avoids me making another API call on the RN app by the pk that 'profile' field returns. 
   return UsernameSerializer(obj.profile).data
  
  

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
  # Serializes a profile instance, all of its fields, and gets minimal data on its following and followers
  followers = serializers.SerializerMethodField()
  following = serializers.SerializerMethodField()
  class Meta:
    model = Profile
    fields = ['pk', 'user', 'display_name', 'username', 'profile_image_url', 'bio_text', 'join_date', 'followers', 'following']

  def get_followers(self, obj):
    followers = obj.get_followers()
    # We use a minimal version of the profile serializer to avoid grabbing following-followers of a profile in a loop.
    # What if two profile's follow each other? We would recursively keep grabbing their follow relations over and over --> mini profile serializer to avoid this
    return ProfileMiniSerializer(followers, many=True).data
  
  def get_following(self, obj):
    following = obj.get_following()
    # We use a minimal version of the profile serializer to avoid grabbing following-followers of a profile in a loop.
    # What if two profile's follow each other? We would recursively keep grabbing their follow relations over and over --> mini profile serializer to avoid this
    return ProfileMiniSerializer(following, many=True).data

class ProfileMiniSerializer(serializers.ModelSerializer):
  # Serializes a few of the fields of a profile object
  class Meta:
    model = Profile
    fields = ['pk', 'username', 'display_name']

class UsernameSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['username']

class PhotoSerializer(serializers.ModelSerializer):
  # Serializes a photo object and all of its fields
  class Meta: 
    model=Photo
    fields=['pk', 'post','image_url','timestamp','image_file']


# ---- User Auth -----
class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  display_name = serializers.CharField(write_only=True, required=False, default='')
  profile_image_url = serializers.URLField(write_only=True, required=False, default='')
  bio_text = serializers.CharField(write_only=True, required=False, default='')
  #password = serializers.CharField(write_only=True)
  class Meta:
    model=User
    fields = ['username', 'password', 'email', 'display_name', 'profile_image_url', 'bio_text']
  
  def create(self, validated_data):
    user = User.objects.create_user(
      username = validated_data['username'],
      password = validated_data['password'],
      email = validated_data['email'],
    )
    
    profile = Profile.objects.create(
      user = user,
      display_name = validated_data['display_name'],
      username = validated_data['username'],
      profile_image_url = validated_data['profile_image_url'],
      bio_text = validated_data['bio_text'],
    )
    
    return user

class MeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Profile
        fields = ['id','user_id','username','display_name','bio_text','profile_image_url', 'join_date']