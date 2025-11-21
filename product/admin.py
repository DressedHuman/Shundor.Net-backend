
from django.contrib import admin
from .models import Product, ProductVariant

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "brand", "category", "is_active")
	search_fields = ("name", "brand__name", "category__name")

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
	list_display = ("product", "sku", "price", "stock", "is_active")
	search_fields = ("product__name", "sku")

