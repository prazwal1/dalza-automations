from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone_number', 'role', 'is_active', 'is_staff', 'created_at', 'updated_at')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'name', 'phone_number')
    ordering = ('email',)
    readonly_fields = ('created_at', 'updated_at')