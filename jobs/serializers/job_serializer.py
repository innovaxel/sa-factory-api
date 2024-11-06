# """
# Serializers for the `Job` model.

# This module contains the `JobSerializer` class, which is used to serialize
# and deserialize `Job` model instances. The `JobSerializer` class converts
# `Job` instances to and from JSON format, including fields such as `id`, `name`,
# `number`, `address_id`, `customerid`, `worklistid`, and `chip`. Related fields
# are represented using primary key references.
# """

# from __future__ import annotations

# from rest_framework import serializers

# from accounts.serializers import SimpleUserSerializer
# from jobs.models import Job, JobLog

# from .job_address_serializer import JobAddressSerializer
# from .customer_serializer import CustomerSerializer
# from .chip_serializer import ChipSerializer


# class JobSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the `Job` model.

#     Converts `Job` model instances into JSON and vice versa.
#     Includes related serializers for `address_id`, `customerid`,
#     and `chip` for complete data representation.
#     """
#     address = JobAddressSerializer(source='address_id')
#     customer = CustomerSerializer(source='customerid')
#     chip = ChipSerializer()

#     class Meta:
#         """
#         Metadata for the `JobSerializer`.

#         Specifies the model to be serialized and the fields to include in the
#         serialized representation.
#         """
#         model = Job
#         fields = [
#             'id', 'name', 'number', 'address',
#             'customer', 'chip', 'status',
#         ]


# class JobLogSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the JobLog model.

#     This serializer includes the user information through the SimpleUserSerializer.
#     """
#     user = SimpleUserSerializer()

#     class Meta:
#         """
#         Meta options for the JobLogSerializer.

#         Specifies the model to be used with this serializer and the fields to be included.
#         """
#         model = JobLog
#         fields = ['user']


from rest_framework import serializers
from jobs.models import AsanaTask
import random
import string


def generate_random_id(length=6):
    """Generate a random string of fixed length for ID."""
    return "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )


class AsanaTaskSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    chip = serializers.SerializerMethodField()

    class Meta:
        model = AsanaTask
        fields = [
            "id",
            "name",
            "number",
            "chip",
            "address",
            "status",
            "customer",
        ]

    id = serializers.CharField(source="task_gid")
    name = serializers.CharField(source="task_name")
    number = serializers.UUIDField(source="task_gid")

    def get_address(self, obj):
        address = {
            "id": "ddf85998-0c53-485d-b798-072b8c59263a",
            "address": "123 Cove Street Prahan",
            "latitude": "0.000003",
            "longitude": "-0.000001",
        }
        return address

    def get_customer(self, obj):
        customer = {
            "id": "69bf5dac-6cb6-4f67-9a12-e1198a775f00",
            "name": "Customer 1",
        }
        return customer

    def get_status(self, obj):
        return "in_progress"

    def get_chip(self, obj):
        # Mapping of chips to colors and texts
        chip_mapping = {
            "External": {"color": "#73EC8B", "text": "green"},
            "REWORK": {"color": "#FF0000", "text": "red"},
            "GARAGE": {"color": "#0000FF", "text": "blue"},
            "H/R": {"color": "#CF2A45FF", "text": "pink"},
            "S/S": {"color": "#CF2A45FF", "text": "pink"},
            "SCREEN": {"color": "#FFA500", "text": "orange"},
            "SPLIT": {"color": "#FFA500", "text": "orange"},
            "STEEL TRAY": {"color": "#FFA500", "text": "orange"},
            "T-1": {"color": "#1AB338FF", "text": "green"},
            "T-2": {"color": "#1AB338FF", "text": "green"},
            "T-3": {"color": "#1AB338FF", "text": "green"},
            "T-4": {"color": "#0000FF", "text": "blue"},
            "T-5": {"color": "#0000FF", "text": "blue"},
            "T-6": {"color": "#FFA500", "text": "orange"},
            "T-7": {"color": "#FFA500", "text": "orange"},
            "T-8": {"color": "#CF2A45FF", "text": "pink"},
            "T-8-hamp": {"color": "#CF2A45FF", "text": "pink"},
            "T-9": {"color": "#FF0000", "text": "red"},
            "T-10": {"color": "#FF0000", "text": "red"},
        }

        # Get the chip name from the object
        chip_name = (
            obj.stair_catery
        )  # Adjust according to your model field name
        chip_data = chip_mapping.get(chip_name)

        if chip_data:
            return {
                "id": generate_random_id(),
                "color": chip_data["color"],
                "text": obj.stair_catery,
                "icon": None,
            }
        else:
            return None  # Return None or handle as necessary if chip name is not found
