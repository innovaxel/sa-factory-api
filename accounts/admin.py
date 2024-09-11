"""
Django admin configuration for managing the User and Devices model.
"""
from __future__ import annotations

from django.contrib import admin

from accounts.models import Devices
from accounts.models import User

class UserAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the User model.

    This class defines how the User model is displayed
    and managed in the Django admin interface,
    including the fields to be displayed, searchable, and filterable.
    """
    list_display = (
        'id', 'username', 'created_at', 'updated_at',
        'deleted_at', 'is_active', 'is_staff',
    )
    search_fields = ('username', 'id')
    list_filter = ('is_active', 'is_staff', 'deleted_at')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')

    def get_fields(self, request, obj=None):
        """
        Return a list of fields to be displayed in the admin interface.
        If no object is provided (i.e., when creating a new user),
        show only 'pin' and 'username'. For existing objects, show all fields.
        """
        return ('pin', 'username')

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.
        If an existing object is being edited, the username field
        will also be read-only.
        """
        if obj:
            return self.readonly_fields + ('username',)
        return self.readonly_fields

class DevicesAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Devices model.
    """
    list_display = ('id', 'api_token', 'created_at', 'updated_at')
    search_fields = ('api_token', 'id')
    list_filter = ('created_at', 'updated_at')
    ordering = ('created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        """
        Return a list of fields that are read-only in the admin interface.
        """
        return self.readonly_fields


admin.site.register(Devices, DevicesAdmin)
admin.site.register(User, UserAdmin)
