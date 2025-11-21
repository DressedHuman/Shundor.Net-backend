
from django.contrib import admin
from .models import SMTPMail

@admin.register(SMTPMail)
class SMTPMailAdmin(admin.ModelAdmin):
	list_display = ("host", "username", "is_active")
	search_fields = ("host", "username")