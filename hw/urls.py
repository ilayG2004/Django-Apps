from django.urls import path
from django.conf import settings
from . import views

#URL patterns specific to the hw app:

urlpatterns = [
  #Connects empty string to views.home
  path(r'', views.home_page, name="home_page"),
  path(r'about', views.about, name="about_page"),
]
