"""
This module defines custom permissions for the Django REST Framework views.

Permissions included:
- `IsAdminOrReadOnly`: Grants full access to admin users and read-only access
  to authenticated simple users.
- `IsAdminOnly`: Grants access only to admin users.
""""""
This module defines custom permissions for the Django REST Framework views.

Permissions included:
- `IsAdminOrReadOnly`: Grants full access to admin users and read-only access
  to authenticated simple users.
- `IsAdminOnly`: Grants access only to admin users.
"""
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from common.device_validator import DeviceValidator


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to grant full access to admin users
    and read-only access to simple users.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return False


class IsAdminOnly(BasePermission):
    """
    Custom permission to grant access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsAuthenticatedAndDeviceValid(BasePermission):
    """
    Custom permission to check if the user is authenticated and the device ID is valid.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        device_id = request.data.get('device_id') if request.data else None

        if device_id:
            try:
                validator = DeviceValidator(device_id)
                validator.validate()
            except PermissionDenied:
                return False

        return True
