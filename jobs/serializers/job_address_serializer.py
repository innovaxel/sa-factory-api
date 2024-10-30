# """
# Serializers for the `JobAddress` model.

# This module contains the `JobAddressSerializer` class, which is used to serialize
# and deserialize `JobAddress` model instances. The `JobAddressSerializer` class
# converts `JobAddress` instances to and from JSON format, including fields such as
# `id`, `address`, `latitude`, and `longitude`.
# """
# from __future__ import annotations

# from rest_framework import serializers

# from jobs.models import JobAddress


# class JobAddressSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the `JobAddress` model.

#     Converts `JobAddress` model instances into JSON and vice versa.
#     Includes the fields `id`, `address`, `latitude`, and `longitude`.
#     """
#     class Meta:
#         model = JobAddress
#         fields = ['id', 'address', 'latitude', 'longitude']
