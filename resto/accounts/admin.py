from django.contrib import admin

from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone", "address", "created_at")
    list_filter = ("user", "created_at")
    search_fields = ("user", "address")
