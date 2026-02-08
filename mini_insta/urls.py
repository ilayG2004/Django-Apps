from django.urls import path
from .views import ProfileListView, ProfileDetailView

urlpatterns = [
  path('', ProfileListView.as_view(), name="show_all_profiles"),
  path('profile/<str:pk>', ProfileDetailView.as_view(), name="show_profile")
]