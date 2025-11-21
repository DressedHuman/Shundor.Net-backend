"""
URL patterns for the product app.
Routes for product and product variant endpoints.
"""
from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView, create_product_with_variants, ProductUpdateView,
    ProductVariantListView, ProductVariantDetailView, ProductVariantUpdateView
)

urlpatterns = [
    # Products
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/create/", create_product_with_variants, name="product-create"),
    path("products/<int:id>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/<int:id>/update/", ProductUpdateView.as_view(), name="product-update"),

    # Variants
    path("products/variants/", ProductVariantListView.as_view(), name="variant-list"),
    path("variants/<int:pk>/", ProductVariantDetailView.as_view(), name="variant-detail"),
    path("variants/<int:pk>/update/", ProductVariantUpdateView.as_view(), name="variant-update"),
]
