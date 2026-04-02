from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


# References view methods
urlpatterns = [
  path('', , name="form"),
  path('result', , name="result"),
]