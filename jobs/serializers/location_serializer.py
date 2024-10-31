# """
# Serializer module for `Location` model.

# This module defines the `LocationSerializer` class, which serializes
# and deserializes instances of the `Location` model.
# """
# from __future__ import annotations

# from rest_framework import serializers

# from jobs.models import Location
# from jobs.serializers.worklist_serializer import WorkListSerializer


# class LocationSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the `Location` model.

#     Converts `Location` model instances into JSON and vice versa.
#     Includes the fields `id` and `name`.
#     """

#     worklists = WorkListSerializer(many=True, read_only=True)

#     class Meta:
#         """
#         Metadata for the `LocationSerializer`.

#         Specifies the model to be serialized and the fields to include in the
#         serialized representation.
#         """
#         model = Location
#         fields = ['id', 'name', 'worklists']

import hashlib
from rest_framework import serializers
from jobs.models import Branch, ResourceGroup
from accounts.serializers import HumanResourceSerializer
from .resource_group_serializer import ResourceGroupSerializer


class BranchSerializer(serializers.ModelSerializer):
    worklists = serializers.SerializerMethodField()
    # users = HumanResourceSerializer(
    #     many=True, read_only=True, source="humanresource_set"
    # )

    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "branch_id",
            # "state",
            "worklists",
        ]

    id = serializers.CharField(source="branch_name")
    name = serializers.CharField(source="branch_name")
    branch_id = serializers.UUIDField(source="branch_guid")
    # state = serializers.CharField()

    def get_worklists(self, instance):
        all_resource_groups = ResourceGroup.objects.all()
        return ResourceGroupSerializer(all_resource_groups, many=True).data

    def to_representation(self, instance):
        """Override to return the branch name's hash as the id."""
        representation = super().to_representation(instance)
        branch_name = representation["id"]
        representation["id"] = hashlib.sha256(branch_name.encode()).hexdigest()
        return representation
