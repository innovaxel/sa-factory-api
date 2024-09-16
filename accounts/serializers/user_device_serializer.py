"""
Serializer module for handling UserDevice data.

This module contains the UserDeviceSerializer which is responsible
for serializing and deserializing UserDevice model instances.
"""
from __future__ import annotations

from rest_framework import serializers

from accounts.models import UserDevice


class UserDeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserDevice model.

    This serializer converts UserDevice model instances into JSON
    and vice versa. It includes fields 'user' and 'device'.
    """

    class Meta:
        """
        Metadata for the UserDeviceSerializer.

        Specifies the model that this serializer works with and
        the fields that should be included in the serialization/deserialization
        process.
        """
        model = UserDevice
        fields = ['user', 'device']
