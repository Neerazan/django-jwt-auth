from django.contrib import admin

from .models import *



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff', 'is_active', 'is_superuser']
    list_filter = ['id' ,'username', 'is_staff', 'is_active']
    fieldsets = (
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'date_joined', 'last_login')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')
        }),
        ('User Credential', {
            'fields': ('username', 'password')
        })
    )

    search_fields = ['username']