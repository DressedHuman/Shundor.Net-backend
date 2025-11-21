"""
URL patterns for the review app.
Routes for review and review status endpoints.
"""
from django.urls import path

from .views import ReviewAPIView

urlpatterns = [
    path("reviews/", ReviewAPIView.as_view(), name="review-list"),
    path("reviews/<int:pk>/", ReviewAPIView.as_view(), name="review-detail"),
]
