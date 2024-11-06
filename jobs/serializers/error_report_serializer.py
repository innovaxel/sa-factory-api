from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.models.human_resource import HumanResource
from jobs.models import (
    ErrorReport,
    ErrorReportImage,
    ErrorReportError,
    AsanaTask,
    ResourceGroup,
    Error,
)


class ErrorReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorReport
        fields = [
            "error_report_id",
            "reported_at_department",
            "hr_id",
            "task_gid",
            "reported_at_time",
            "comments",
        ]
        read_only_fields = ["error_report_id", "reported_at_time"]


class ErrorReportErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorReportError
        fields = ["error_report_id", "error_id"]


class ErrorReportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorReportImage
        fields = ["error_report_id", "image_url"]


class ErrorReportCreateSerializer(serializers.Serializer):
    reported_at_department = serializers.IntegerField()
    hr_id = serializers.IntegerField()
    task_gid = serializers.CharField(max_length=50)
    comments = serializers.CharField(allow_blank=True, required=False)
    errors = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    images = serializers.ListField(
        child=serializers.CharField(), required=False
    )

    def create(self, validated_data):
        try:
            reported_at_department_id = validated_data.pop(
                "reported_at_department"
            )
            hr_id = validated_data.pop("hr_id")
            task_gid_value = validated_data.pop("task_gid")

            # Debug: Log IDs and lookups
            print(
                f"Looking up ResourceGroup with ID: {reported_at_department_id}"
            )
            reported_at_department = get_object_or_404(
                ResourceGroup, pk=reported_at_department_id
            )

            print(f"Looking up HumanResource with ID: {hr_id}")
            hr = get_object_or_404(HumanResource, pk=hr_id)

            print(f"Looking up AsanaTask with GID: {task_gid_value}")
            task_gid = get_object_or_404(AsanaTask, pk=task_gid_value)

            error_report = ErrorReport.objects.create(
                reported_at_department=reported_at_department,
                hr_id=hr,
                task_gid=task_gid,
                comments=validated_data.get("comments", ""),
            )

            errors = validated_data.pop("errors", [])
            images = validated_data.pop("images", [])

            for error_id in errors:
                print(f"Looking up Error with ID: {error_id}")
                error_instance = get_object_or_404(Error, pk=error_id)
                ErrorReportError.objects.create(
                    error_report_id=error_report, error_id=error_instance
                )

            for image_url in images:
                ErrorReportImage.objects.create(
                    error_report_id=error_report, image_url=image_url
                )

            return error_report

        except Exception as e:
            print(f"An error occurred: {e}")
            raise
