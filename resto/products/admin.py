from django.contrib import admin

from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price", "menu_order", "created_at")
    list_filter = ("name", "created_at")
    search_fields = ("name", "price")
