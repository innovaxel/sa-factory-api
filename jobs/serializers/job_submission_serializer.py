"""
Serializer for the `JobSubmission` model.

This module contains the `JobSubmissionSerializer` class, which is used to serialize
and deserialize `JobSubmission` model instances. The `JobSubmissionSerializer` class
converts `JobSubmission` instances to and from JSON format, including fields such as
`id`, `comment`, and `job_id`.
"""
from rest_framework import serializers
from jobs.models import JobSubmission, Job

class JobSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for the `JobSubmission` model.
    Converts `JobSubmission` instances to JSON and vice versa.
    """
    job_id = serializers.UUIDField()

    class Meta:
        """
        Meta configuration for the `JobSubmissionSerializer`.

        Specifies the model to be serialized (`JobSubmission`) and the fields 
        to be included in the serialization and deserialization processes. 
        Includes `id`, `comment`, and `job_id` fields.
        """
        model = JobSubmission
        fields = ['id', 'comment', 'job_id']

    def validate_job(self, value):
        """
        Convert the job UUID into a Job instance.
        """
        try:
            job_instance = Job.objects.get(id=value)
        except Job.DoesNotExist:
            raise serializers.ValidationError(
                "Job with this ID does not exist."
                )
        return job_instance
