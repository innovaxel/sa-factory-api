"""
Serializers for the `ErrorSubCategory` model.

This module contains the `ErrorSubCategorySerializer` class, which is used to serialize
and deserialize `ErrorSubCategory` model instances. The `ErrorSubCategorySerializer` class
converts `ErrorSubCategory` instances to and from JSON format, including fields such as 
`id`, `name`, `code`, and `error_category`.
"""

from rest_framework import serializers
from jobs.models import ErrorSubCategory

class ErrorSubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the `ErrorSubCategory` model.

    Converts `ErrorSubCategory` model instances into JSON and vice versa. 
    Includes the fields `id`, `name`, `code`, and `error_category`.
    """

    class Meta:
        """
        Metadata for the `ErrorSubCategorySerializer`.

        Specifies the model to be serialized and the fields to include in the
        serialized representation.
        """
        model = ErrorSubCategory
        fields = ['id', 'name', 'code', 'error_category']
