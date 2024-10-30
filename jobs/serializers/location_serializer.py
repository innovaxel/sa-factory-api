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
