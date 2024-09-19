"""
This module contains serializers for user registration and login.

It defines:
- `UserRegistrationSerializer`: A serializer for handling user registration,
    including validation and user creation with a hashed PIN.
- `LoginSerializer`: A serializer for handling user login,
    validating API tokens and PINs.
"""
from __future__ import annotations

from django.contrib.auth import authenticate
from rest_framework import serializers


class AdminLoginSerializer(serializers.Serializer):
    """
    Serializer for admin login with username and password validation.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError(
                'Both username and password are required.',
            )

        user = authenticate(username=username, password=password)
        if user is None or not user.is_staff:
            raise serializers.ValidationError(
                'Invalid username or password, or user is not an admin.',
            )
        return attrs

    def create(self, validated_data):
        raise NotImplementedError('Create method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Update method not implemented')


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


class DeviceAuthenticationSerializer(serializers.Serializer):
    """
    Serializer to validate the incoming data for device ID and PIN.
    """
    device_id = serializers.CharField(required=True)
    pin = serializers.CharField(write_only=True, required=True)


class DeviceRegistrationInputSerializer(serializers.Serializer):
    """
    Serializer for handling device registration input data.

    Validates the API key and device ID.
    """
    api_key = serializers.CharField(max_length=255)
    device_id = serializers.CharField(max_length=255)


class SetPinSerializer(serializers.Serializer):
    """
    Serializer for setting the PIN for a `SimpleUser`.

    Validates the device ID and the new PIN value.
    """
    device_id = serializers.CharField(max_length=255)
    pin = serializers.CharField(max_length=4, min_length=4)

    def validate_pin(self, value):
        """
        Ensure that the PIN is a valid integer and exactly 4 digits.
        """
        if not value.isdigit():
            raise serializers.ValidationError('PIN must be a valid integer.')
        if len(value) != 4:
            raise serializers.ValidationError('PIN must be exactly 4 digits.')
        return value
