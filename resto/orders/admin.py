from django.contrib import admin

from .models import *

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "total_price", "created_at")
    list_filter = ("user", "created_at")
    search_fields = ("user", "total_price")