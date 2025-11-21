
from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'slug', 'created_at')

admin.site.register(Category, CategoryAdmin)