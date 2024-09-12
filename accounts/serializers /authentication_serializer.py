"""
This module contains serializers for user registration and login.

It defines:
- `UserRegistrationSerializer`: A serializer for handling user registration, 
    including validation and user creation with a hashed PIN.
- `LoginSerializer`: A serializer for handling user login, 
    validating API tokens and PINs.
"""

import hashlib
from rest_framework import serializers
from accounts.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles user creation and validation including generating a default username if not provided.
    """
    pin = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        """
        Metadata for the UserRegistrationSerializer.

        Defines the model to be used and specifies which fields should be included
        in the serialization and deserialization processes.
        """
        model = User
        fields = ['username', 'pin']
        extra_kwargs = {
            'pin': {'write_only': True},
        }

    def validate(self, data):
        """
        Validate the provided data and generate a default username if not provided.

        Parameters:
            data (dict): Input data containing 'username' and 'pin'.

        Returns:
            dict: Validated data with potentially modified 'username'.
        
        Raises:
            serializers.ValidationError: If 'pin' is missing or 'username' is too long.
        """
        pin = data.get('pin')
        if not pin:
            raise serializers.ValidationError("PIN is required")

        if not data.get('username'):
            hash_object = hashlib.sha256(pin.encode())
            hex_dig = hash_object.hexdigest()
            data['username'] = f"{hex_dig[:7]}-username"

        if len(data['username']) > 150:
            raise serializers.ValidationError("Username is too long")

        return data

    def create(self, validated_data):
        """
        Create and return a new user instance with a hashed PIN.

        Parameters:
            validated_data (dict): The validated input data.

        Returns:
            User: The created user instance.
        """
        username = validated_data.get('username')
        pin = validated_data.get('pin')

        user = User(username=username)
        user.set_pin(pin)
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for handling login data.

    Validates the API token and PIN provided by the user.
    """
    api_token = serializers.CharField(max_length=10)
    pin = serializers.CharField(max_length=128)

class UpdatePinSerializer(serializers.Serializer):
    """
    Serializer for handling PIN update data.

    Validates the API token, new PIN, and bearer token.
    """
    api_token = serializers.CharField(max_length=10)
    new_pin = serializers.CharField(max_length=128)
