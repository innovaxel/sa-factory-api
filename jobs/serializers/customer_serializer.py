"""
Serializers for the `Customer` model.

This module contains the `CustomerSerializer` class, which is used to serialize
and deserialize `Customer` model instances. The `CustomerSerializer` class converts
`Customer` instances to and from JSON format, including fields such as `id` and `name`.
"""

from rest_framework import serializers
from jobs.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.

    Attributes:
        id (UUIDField): The unique identifier for the customer.
        name (CharField): The name of the customer.
    """

    class Meta:
        model = Customer
        fields = ['id', 'name']
