from django.urls import path
from .views import (
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView
)

urlpatterns = [
    # List all categories (GET)
    path('categories/', CategoryListView.as_view(), name='category-list'),

    # Create a new category (POST, admin only)
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),

    # Update a category by ID (PUT/PATCH, admin only)
    path('categories/<str:id>/update/', CategoryUpdateView.as_view(), name='category-update'),

    # Delete a category by ID (DELETE, admin only)
    path('categories/<str:id>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
]
