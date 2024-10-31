from rest_framework import serializers
from accounts.models import HumanResource


class HumanResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanResource
        fields = [
            "hr_id",
            "hr_job_title",
            "hr_guid",
            "hr_pin",
            "hr_timesheet_user",
        ]
