"""
Custom authentication backend for
handling SimpleUser model authentication
using full name and PIN.
"""
from __future__ import annotations

from django.contrib.auth.backends import BaseBackend

from .models import SimpleUser


class SimpleUserBackend(BaseBackend):
    """
    Custom authentication backend for SimpleUser
    model using full name and PIN.
    """

    def authenticate(self, request, full_name=None, pin=None, **kwargs):
        """
        Authenticate a user based on full name and PIN.

        Args:
            request: The HTTP request object.
            full_name (str): The full name of the user.
            pin (str): The PIN of the user.

        Returns:
            SimpleUser or None: Returns the user instance
            if authentication is successful, otherwise returns None.
        """
        try:
            user = SimpleUser.objects.get(full_name=full_name)
            if user.check_pin(pin):
                return user
        except SimpleUser.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            SimpleUser or None: Returns the user instance
            if found, otherwise returns None.
        """
        try:
            return SimpleUser.objects.get(pk=user_id)
        except SimpleUser.DoesNotExist:
            return None
