"""
URL configuration for user profile management and reseller/supplier request endpoints.
"""

from django.urls import path
from . import views


urlpatterns = [
    path("user-profile/", views.UserProfileViewSet.as_view(), name="user-profile-list"),
]
