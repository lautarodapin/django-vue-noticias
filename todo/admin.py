from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "title", "is_done", "created_at", "mod_at"]
    list_filter = ["user", "is_done"]
    
