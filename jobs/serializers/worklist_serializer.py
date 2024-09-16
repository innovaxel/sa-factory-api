"""
Serializer module for `WorkList` model.

This module defines the `WorkListSerializer` class, which serializes
and deserializes instances of the `WorkList` model.
"""
from __future__ import annotations

from rest_framework import serializers

from jobs.models import Location
from jobs.models import WorkList


class WorkListSerializer(serializers.ModelSerializer):
    """
    Serializer for the `WorkList` model.

    Converts `WorkList` model instances into JSON and vice versa.
    Includes the fields `id`, `title`, and `location`.
    """
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())

    class Meta:
        """
        Metadata for the `WorkListSerializer`.

        Specifies the model to be serialized and the fields to include in the
        serialized representation.
        """
        model = WorkList
        fields = ['id', 'title', 'location']
