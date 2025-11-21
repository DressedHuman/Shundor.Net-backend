
from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "status", "created_at", "updated_at")
	search_fields = ("user__email", "status")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ("order", "quantity", "price")
	search_fields = ("order__id", "product__name")
