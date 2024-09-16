"""
Serializers for the `ErrorCategory` model.

This module contains the `ErrorCategorySerializer` class, which is used to serialize
and deserialize `ErrorCategory` model instances. The `ErrorCategorySerializer` class
converts `ErrorCategory` instances to and from JSON format, including fields such as 
`id`, `name`, `code`, and nested `subcategories` using the `ErrorSubCategorySerializer`.
"""

from rest_framework import serializers
from jobs.models import ErrorCategory

from .error_subcategory_serializer import ErrorSubCategorySerializer

class ErrorCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ErrorCategory model.

    Converts ErrorCategory model instances into JSON and vice versa.
    Includes the fields `id`, `name`, and `code`.
    """

    subcategories = ErrorSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = ErrorCategory
        fields = ['id', 'name', 'code', 'subcategories']
