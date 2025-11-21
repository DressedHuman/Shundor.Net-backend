
from django.contrib import admin
from .models import ShippingCharge

@admin.register(ShippingCharge)
class ShippingChargeAdmin(admin.ModelAdmin):
	list_display = ("area", "amount", "created_at", "updated_at")
	search_fields = ("area",)