"""
URL patterns for the product app.
Routes for product, product image, size, and color endpoints.
"""
from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView, create_product_with_images, ProductUpdateView,
    ProductImageListView, ProductImageDetailView, ProductImageUpdateView,
    SizeListCreateView, SizeDetailView, SizeUpdateView, SizeDeleteView,
    ColorListCreateView, ColorDetailView, ColorUpdateView, ColorDeleteView
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
    
    # Sizes
    path("sizes/", SizeListCreateView.as_view(), name="size-list-create"),
    path("sizes/<int:pk>/", SizeDetailView.as_view(), name="size-detail"),
    path("sizes/<int:pk>/update/", SizeUpdateView.as_view(), name="size-update"),
    path("sizes/<int:pk>/delete/", SizeDeleteView.as_view(), name="size-delete"),
    
    # Colors
    path("colors/", ColorListCreateView.as_view(), name="color-list-create"),
    path("colors/<int:pk>/", ColorDetailView.as_view(), name="color-detail"),
    path("colors/<int:pk>/update/", ColorUpdateView.as_view(), name="color-update"),
    path("colors/<int:pk>/delete/", ColorDeleteView.as_view(), name="color-delete"),
]

