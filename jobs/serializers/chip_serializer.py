"""
Serializers for the `Chip` model.

This module contains the `ChipSerializer` class used to serialize and deserialize
`Chip` model instances. The `ChipSerializer` class converts `Chip` instances to and from
JSON format, including fields such as `id`, `color`, `text`, and `icon`.
"""
from __future__ import annotations

from rest_framework import serializers

from jobs.models import Chip


class ChipSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Chip` model.

    Converts `Chip` model instances into JSON and vice versa.
    Includes the fields `id`, `color`, `text`, and `icon`.
    """

    class Meta:
        """
        Metadata for the `ChipSerializer`.

        Specifies the model to be serialized and the fields to include in the
        serialized representation.
        """
        model = Chip
        fields = ['id', 'color', 'text', 'icon']
