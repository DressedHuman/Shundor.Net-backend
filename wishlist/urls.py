
"""
URL configuration for the Wishlist app, mapping endpoints to wishlist views.
"""
from django.urls import path
from .views import WishlistListCreateAPIView, WishlistDetailAPIView

urlpatterns = [
    path("wishlist/", WishlistListCreateAPIView.as_view(), name="wishlist-list-create"),
    path("wishlist/<str:pk>/", WishlistDetailAPIView.as_view(), name="wishlist-detail"),
]
