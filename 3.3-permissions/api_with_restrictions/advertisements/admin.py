from django.contrib import admin
from .models import Advertisement


@admin.register(Advertisement)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status', 'creator', 'created_at', 'updated_at' ]
    list_filter = ['id', 'title']
