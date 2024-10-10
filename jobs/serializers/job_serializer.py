"""
Serializers for the `Job` model.

This module contains the `JobSerializer` class, which is used to serialize
and deserialize `Job` model instances. The `JobSerializer` class converts
`Job` instances to and from JSON format, including fields such as `id`, `name`,
`number`, `address_id`, `customerid`, `worklistid`, and `chip`. Related fields
are represented using primary key references.
"""

from __future__ import annotations

from rest_framework import serializers

from accounts.serializers import SimpleUserSerializer
from jobs.models import Job, JobLog

from .job_address_serializer import JobAddressSerializer
from .customer_serializer import CustomerSerializer
from .chip_serializer import ChipSerializer


class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Job` model.

    Converts `Job` model instances into JSON and vice versa.
    Includes related serializers for `address_id`, `customerid`,
    and `chip` for complete data representation.
    """
    address = JobAddressSerializer(source='address_id')
    customer = CustomerSerializer(source='customerid')
    chip = ChipSerializer()

    class Meta:
        """
        Metadata for the `JobSerializer`.

        Specifies the model to be serialized and the fields to include in the
        serialized representation.
        """
        model = Job
        fields = [
            'id', 'name', 'number', 'address',
            'customer', 'chip', 'status',
        ]


class JobLogSerializer(serializers.ModelSerializer):
    """
    Serializer for the JobLog model.

    This serializer includes the user information through the SimpleUserSerializer.
    """
    user = SimpleUserSerializer()

    class Meta:
        """
        Meta options for the JobLogSerializer.

        Specifies the model to be used with this serializer and the fields to be included.
        """
        model = JobLog
        fields = ['user']
