"""
This module contains serializers for the `SimpleUser` model.

The `SimpleUserSerializer` is responsible for converting `SimpleUser` model
instances into JSON and vice versa. It includes additional methods to compute
fields like `time_spent` and `pin_set`.
"""

from rest_framework import serializers
from accounts.models import SimpleUser


class SimpleUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the `SimpleUser` model.

    Converts `SimpleUser` model instances into JSON and vice versa.
    Includes the fields `id`, `full_name`, `role`, `time_spent`, and `pin_set`.
    """
    time_spent = serializers.SerializerMethodField()
    pin_set = serializers.SerializerMethodField()

    class Meta:
        """
        Metadata for the `SimpleUserSerializer`.

        Specifies the model to be serialized and the fields to include
        in the serialized representation.
        """
        model = SimpleUser
        fields = ['id', 'full_name', 'role', 'time_spent', 'pin_set']

    def get_time_spent(self, obj):
        """
        Custom method to get the value for the `time_spent` field.
        """
        return '5'

    def get_pin_set(self, obj):
        """
        Custom method to get the value for the `pin_set` field.
        """
        return obj.pin is not None and obj.pin != ''
