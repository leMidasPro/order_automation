from django.contrib import admin

from .models import *

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "step", "selected_product", "quantity", "created_at")
    list_filter = ("phone_number", "created_at")
    search_fields = ("phone_number", "quantity")