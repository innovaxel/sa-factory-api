"""
Serializer module for handling SimpleUser data.

This module contains the UserSerializer which is responsible
for serializing and deserializing SimpleUser model instances.
"""

from rest_framework import serializers
from accounts.models import SimpleUser

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the SimpleUser model.

    This serializer converts SimpleUser model instances into JSON
    and vice versa. It includes fields 'full_name' and 'pin'.
    """

    class Meta:
        """
        Metadata for the UserSerializer.

        Specifies the model that this serializer works with and
        the fields that should be included in the serialization/deserialization
        process.
        """
        model = SimpleUser
        fields = ['full_name', 'pin']
