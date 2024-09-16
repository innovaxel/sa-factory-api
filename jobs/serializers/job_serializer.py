"""
Serializers for the `Job` model.

This module contains the `JobSerializer` class, which is used to serialize
and deserialize `Job` model instances. The `JobSerializer` class converts
`Job` instances to and from JSON format, including fields such as `id`, `name`,
`number`, `address_id`, `customerid`, `worklistid`, and `chip`. Related fields
are represented using primary key references.
"""

from rest_framework import serializers
from jobs.models import Job
from jobs.models import Customer, JobAddress, WorkList, Chip

class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Job` model.

    Converts `Job` model instances into JSON and vice versa. 
    Includes the fields `id`, `name`, `number`, `address_id`,
    `customerid`, `worklistid`, and `chip`.
    """

    address_id = serializers.PrimaryKeyRelatedField(queryset=JobAddress.objects.all())
    customerid = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    worklistid = serializers.PrimaryKeyRelatedField(queryset=WorkList.objects.all())
    chip = serializers.PrimaryKeyRelatedField(queryset=Chip.objects.all())

    class Meta:
        """
        Metadata for the `JobSerializer`.

        Specifies the model to be serialized and the fields to include in the
        serialized representation.
        """
        model = Job
        fields = ['id', 'name', 'number', 'address_id', 'customerid', 'worklistid', 'chip']
