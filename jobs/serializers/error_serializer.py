# """
# Serializer for handling `Error` model data.

# This module includes:
# - `ErrorSerializer`: Serializes `Error` model instances, converting
# UUIDs to related `Job` and `ErrorSubCategory` instances.
# """

# import uuid
# from rest_framework import serializers
# from jobs.models import Error, Job, ErrorSubCategory


# class ErrorSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the Error model, handling the serialization
#     of error-related data, including the associated user, job,
#     and error subcategory.
#     """
#     job_id = serializers.UUIDField()
#     errorsubcategories = serializers.PrimaryKeyRelatedField(
#         queryset=ErrorSubCategory.objects.all(),
#         many=True,
#     )

#     class Meta:
#         model = Error
#         fields = ['id', 'errorsubcategories', 'comment', 'job_id']
#         read_only_fields = ['id', 'user']

#     def validate_errorsubcategories(self, value):
#         """
#         Validate the errorsubcategories field to ensure it
#         contains valid UUIDs or ErrorSubCategory instances.
#         """
#         if isinstance(value, str):
#             value = value.strip('[]').replace('"', '').split(',')

#         if not all(
#             isinstance(subcategory, (ErrorSubCategory, uuid.UUID))
#             for subcategory in value
#         ):
#             raise serializers.ValidationError(
#                 'Invalid errorsubcategories. Must be \
#                     UUIDs or ErrorSubCategory instances.',
#             )

#         return value

#     def create(self, validated_data):
#         job_id = validated_data.pop('job_id')
#         try:
#             job_instance = Job.objects.get(id=job_id)
#         except Job.DoesNotExist:
#             raise serializers.ValidationError('Job with the given ID does not exist.')

#         subcategories_data = validated_data.pop('errorsubcategories')
#         error = Error.objects.create(job=job_instance, **validated_data)
#         error.errorsubcategories.set(subcategories_data)

#         return error

#     def update(self, instance, validated_data):
#         job_id = validated_data.pop('job_id', None)
#         if job_id:
#             try:
#                 job_instance = Job.objects.get(id=job_id)
#                 instance.job = job_instance
#             except Job.DoesNotExist:
#                 raise serializers.ValidationError(
#                     'Job with the given ID does not exist.',
#                 )

#         subcategories_data = validated_data.pop('errorsubcategories', None)
#         if subcategories_data is not None:
#             instance.errorsubcategories.set(subcategories_data)

#         instance.comment = validated_data.get('comment', instance.comment)
#         instance.save()

#         return instance
