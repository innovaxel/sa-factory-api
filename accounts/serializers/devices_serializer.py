"""
Serializers for the `Devices` model.

This module contains the `DevicesSerializer` class, 
which is used to serialize and deserialize `Devices` objects.
"""

from rest_framework import serializers
from accounts.models import Devices

class DevicesSerializer(serializers.ModelSerializer):
    """
    Serializer class for Devices model.

    Attributes:
        model (class): The model class to be serialized.
        fields (list): The fields to be included in the serialized representation.

    """
    class Meta:
        """
        The Meta class for the DevicesSerializer.

        Attributes:
            model (Model): The model class associated with the serializer.
            fields (list): The list of fields to include in the serialized representation.
        """

        model = Devices
        fields = ['api_key', 'device_id', 'api_url']
