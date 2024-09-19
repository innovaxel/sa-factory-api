"""
Django admin configuration for managing the User and Devices model.
"""
from __future__ import annotations

from django.contrib import admin

from django.contrib.auth.hashers import make_password

from accounts.models import (
    Devices,
    SimpleUser,
    UserDevice,
)


class SimpleUserAdmin(admin.ModelAdmin):
    """
    Admin interface for the SimpleUser model.

    This class customizes the display and functionality of the SimpleUser model
    in the Django admin interface.
    """
    list_display = (
        'id', 'username', 'full_name', 'pin',
        'role', 'is_staff', 'created_at', 'updated_at',
    )
    search_fields = ('full_name',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    def get_form(self, request, obj=None, change=False, **kwargs):
        """
        Use a custom form for adding users to display only the required fields.
        """
        if obj is None:
            kwargs['fields'] = ('pin', 'full_name', 'workilist_id')
        else:
            kwargs['fields'] = (
                'id', 'full_name', 'pin', 'role',
                'workilist_id', 'is_staff', 'created_at', 'updated_at',
            )
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        Override save_model to ensure the password is hashed.
        """
        if not change:
            if obj.pin:
                obj.password = make_password(obj.pin)
        super().save_model(request, obj, form, change)


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
