"""
Serializer module for `WorkList` model.

This module defines the `WorkListSerializer` class, which serializes
and deserializes instances of the `WorkList` model.
"""

from __future__ import annotations

from rest_framework import serializers

from jobs.models import (
    Location,
    WorkList,
)

from accounts.models import SimpleUser
from accounts.serializers import SimpleUserSerializer


class WorkListSerializer(serializers.ModelSerializer):
    """
    Serializer for the `WorkList` model.
    """

    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
    )
    users = serializers.SerializerMethodField()

    class Meta:
        model = WorkList
        fields = ['id', 'title', 'location_id', 'users']

    def get_users(self, obj):
        """
        Get the list of users associated with this work list.
        """
        users = SimpleUser.objects.filter(workilist_id=obj.id)
        return SimpleUserSerializer(users, many=True).data
