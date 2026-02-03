from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
  path(r'', views.main_page, name="main_page"),
  path(r'main', views.main_page, name="main_page"),
  path(r'order', views.order_form, name="order_form"),
  path(r'confirmation', views.submit_order, name="submit_order")
]