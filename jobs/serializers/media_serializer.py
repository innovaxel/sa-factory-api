"""
Serializers for the `Media` model.

This module contains the `MediaSerializer` class, which is used to serialize
and deserialize `Media` model instances. The `MediaSerializer` class
converts `Media` instances to and from JSON format, including fields such as
`id` and `image`.
"""

from rest_framework import serializers
from jobs.models import Media


class MediaSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Media` model.

    Converts `Media` model instances into JSON and vice versa.
    Includes the fields `id` and `image`.
    """

    class Meta:
        """
        Meta configuration for the `MediaSerializer`.

        Specifies the model to be serialized (`Media`) and the fields
        to be included in the serialization and deserialization processes.
        Includes `id` and `image` fields.
        """
        model = Media
        fields = ['id', 'image']
