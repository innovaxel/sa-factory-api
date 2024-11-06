from rest_framework import serializers
from jobs.models import ErrorGroup, Error, ErrorGroupError


class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Error
        fields = [
            "id",
            "name",
            "error_department",
        ]

    id = serializers.CharField(source="error_id")
    name = serializers.CharField(source="error_desc")
    error_department = serializers.UUIDField()


class ErrorGroupSerializer(serializers.ModelSerializer):
    errors = serializers.SerializerMethodField()

    class Meta:
        model = ErrorGroup
        fields = [
            "id",
            "name",
            "errors",
        ]

    id = serializers.CharField(source="error_group_id")
    name = serializers.CharField(source="error_group_name")

    def get_errors(self, obj):
        error_ids = ErrorGroupError.objects.filter(
            error_group_id=obj
        ).values_list("error_id", flat=True)
        errors = Error.objects.filter(error_id__in=error_ids)
        return ErrorSerializer(errors, many=True).data
