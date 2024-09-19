"""
Serializer for handling `Error` model data.

This module includes:
- `ErrorSerializer`: Serializes `Error` model instances, converting
UUIDs to related `Job` and `ErrorSubCategory` instances.
"""


from rest_framework import serializers
from jobs.models import Error, Job, ErrorSubCategory


class ErrorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Error model, handling the serialization
    of error-related data, including the associated user, job,
    and error subcategory.
    """
    job_id = serializers.UUIDField()
    errorsubcategory_id = serializers.UUIDField()

    class Meta:
        """
        Meta class for `ErrorSerializer`.

        Defines the model to be used and the fields to be included in
        serialization/deserialization.

        Attributes:
            model (Model): The model class associated with this serializer (`Error`).
            fields (list): List of fields to be included in the serialized output.
            read_only_fields (list): List of fields that are read-only and
            cannot be modified by the user.
        """
        model = Error
        fields = ['id', 'errorsubcategory_id', 'comment', 'job_id']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        """
        Override the create method to handle UUID to Job and
        ErrorSubCategory instance conversion.
        """
        job_id = validated_data.pop('job_id')
        errorsubcategory_id = validated_data.pop('errorsubcategory_id')
        user = validated_data.pop('user')

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            raise serializers.ValidationError({'job': 'Invalid job ID.'})

        try:
            errorsubcategory = ErrorSubCategory.objects.get(id=errorsubcategory_id)
        except ErrorSubCategory.DoesNotExist:
            raise serializers.ValidationError(
                {
                    'errorsubcategory': 'Invalid error subcategory ID.',
                },
            )

        error = Error.objects.create(
            job=job, user=user, errorsubcategory=errorsubcategory, **validated_data,
        )
        return error
