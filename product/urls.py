"""
URL patterns for the product app.
Routes for product and product image endpoints.
"""
from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView, create_product_with_images, ProductUpdateView,
    ProductImageListView, ProductImageDetailView, ProductImageUpdateView
)

urlpatterns = [
    # Products
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/create/", create_product_with_images, name="product-create"),
    path("products/<int:id>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/<int:id>/update/", ProductUpdateView.as_view(), name="product-update"),

    # Images
    path("products/images/", ProductImageListView.as_view(), name="image-list"),
    path("images/<int:pk>/", ProductImageDetailView.as_view(), name="image-detail"),
    path("images/<int:pk>/update/", ProductImageUpdateView.as_view(), name="image-update"),
]

