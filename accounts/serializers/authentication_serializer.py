"""
This module contains serializers for user registration and login.

It defines:
- `UserRegistrationSerializer`: A serializer for handling user registration,
    including validation and user creation with a hashed PIN.
- `LoginSerializer`: A serializer for handling user login,
    validating API tokens and PINs.
"""
from __future__ import annotations

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Serializer for handling login data.

    Validates the API token and PIN provided by the user.
    """
    api_key = serializers.CharField(max_length=40)
    pin = serializers.CharField(max_length=100)


class UpdatePinSerializer(serializers.Serializer):
    """
    Serializer for handling PIN update data.

    Validates the API token, new PIN, and bearer token.
    """
    api_key = serializers.CharField(max_length=255)
    new_pin = serializers.CharField(max_length=100)


class UserRegistrationInputSerializer(serializers.Serializer):
    """
    Serializer for handling user registration input data.

    Validates the API key, device ID, API URL, full name, and PIN.
    """
    api_key = serializers.CharField(max_length=255)
    device_id = serializers.CharField(max_length=255)
    api_url = serializers.URLField()
    full_name = serializers.CharField(max_length=255)
    pin = serializers.CharField(max_length=100, allow_blank=True, required=False)
