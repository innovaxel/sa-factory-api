"""
Django admin configuration for managing the User and Devices model.
"""
from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User

from accounts.models import Devices
from accounts.models import SimpleUser
from accounts.models import UserDevice


class SimpleUserAdmin(admin.ModelAdmin):
    """
    Admin interface for the SimpleUser model.
    """
    list_display = ('id', 'full_name', 'created_at', 'updated_at')
    search_fields = ('full_name',)
    readonly_fields = ('id', 'created_at', 'updated_at')


class CustomUserAdmin(DefaultUserAdmin):
    """
    Custom admin interface for the default Django User model.
    """
    model = User
    list_display = (
        'id', 'username', 'email', 'first_name',
        'last_name', 'is_staff', 'is_superuser',
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    def get_model_perms(self, request):
        """
        Hide the User model from the admin if the
        user does not have permission to view it.
        """
        if not request.user.is_superuser:
            return {}
        return super().get_model_perms(request)

    def get_queryset(self, request):
        """
        Customize queryset to include only users with specific permissions.
        """
        qs = super().get_queryset(request)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        """
        Customize the form used in the admin interface
        to exclude the username field if not needed.
        """
        form = super().get_form(request, obj, **kwargs)
        if obj:
            # Exclude username field for existing objects if needed
            form.base_fields.pop('username', None)
        return form

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.model._meta.verbose_name = 'Admin'
        self.model._meta.verbose_name_plural = 'Admins'


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


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(SimpleUser, SimpleUserAdmin)
admin.site.register(Devices, DevicesAdmin)
admin.site.register(UserDevice, UserDeviceAdmin)
