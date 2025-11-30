
from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1
	fields = ('image', 'alt_text', 'is_primary', 'order')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "brand", "category", "price", "stock", "is_active")
	search_fields = ("name", "brand__name", "category__name", "sku")
	list_filter = ("is_active", "brand", "category")
	inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
	list_display = ("product", "is_primary", "order", "created_at")
	search_fields = ("product__name",)
	list_filter = ("is_primary",)

