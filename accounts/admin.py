"""
Django admin configuration for managing the User and Devices model.
"""
from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import (
    Devices,
    SimpleUser,
    UserDevice,
    CustomUser,
)


class CustomUserAdmin(UserAdmin):
    """
    Custom admin class to display all fields of the CustomUser model,
    including the id (UUID) field.
    """
    model = CustomUser

    list_display = [
        'id', 'username', 'email', 'is_staff',
        'is_superuser', 'last_login', 'date_joined',
    ]

    list_filter = ['is_staff', 'is_superuser', 'is_active']

    fieldsets = (
        (None, {'fields': ('id', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        (
            'Permissions', {
                'fields': (
                    'is_active', 'is_staff',
                    'is_superuser', 'groups', 'user_permissions',
                ),
            },
        ),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ['id', 'last_login', 'date_joined']


class SimpleUserAdmin(admin.ModelAdmin):
    """
    Admin interface for the SimpleUser model.
    """
    list_display = ('id', 'full_name', 'created_at', 'updated_at')
    search_fields = ('full_name',)
    readonly_fields = ('id', 'created_at', 'updated_at')


class DevicesAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Devices model.

    This class customizes the display and functionality of the Devices model
    in the Django admin interface.
    """
    list_display = ('id', 'device_id', 'api_key', 'created_at', 'updated_at')
    search_fields = ('device_id', 'api_key')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def __str__(self) -> str:
        """
        Returns a string representation of the admin configuration.

        Returns:
            str: A description of the admin configuration.
        """
        return 'Devices Admin Configuration'


class UserDeviceAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserDevice model.

    This class customizes the display and functionality of the UserDevice model
    in the Django admin interface.
    """
    list_display = ('id', 'user', 'device', 'assigned_date')
    search_fields = ('user__username', 'device__api_key')
    list_filter = ('assigned_date', 'user', 'device')
    readonly_fields = ('assigned_date',)

    def __str__(self) -> str:
        """
        Returns a string representation of the admin configuration.

        Returns:
            str: A description of the admin configuration.
        """
        return 'UserDevice Admin Configuration'


admin.site.register(SimpleUser, SimpleUserAdmin)
admin.site.register(Devices, DevicesAdmin)
admin.site.register(UserDevice, UserDeviceAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
