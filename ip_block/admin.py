
from django.contrib import admin
from .models import BlockedIP

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
	list_display = ("ip_number", "created_at", "reason")
	search_fields = ("ip_number", "reason")


