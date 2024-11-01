from rest_framework import serializers
from jobs.models import JobTrackingEntry, ResourceGroup, Branch, AsanaTask
from accounts.models import HumanResource


class JobTrackingEntrySerializer(serializers.ModelSerializer):
    entry_branch_name = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all()
    )
    entry_area_group = serializers.PrimaryKeyRelatedField(
        queryset=ResourceGroup.objects.all()
    )
    entry_hr = serializers.PrimaryKeyRelatedField(
        queryset=HumanResource.objects.all()
    )
    entry_task_gid = serializers.PrimaryKeyRelatedField(
        queryset=AsanaTask.objects.all()
    )

    entry_start_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False
    )
    entry_end_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False
    )

    class Meta:
        model = JobTrackingEntry
        fields = [
            "entry_date",
            "entry_branch_name",
            "entry_area_group",
            "entry_hr",
            "entry_task_gid",
            "entry_job_id",
            "entry_start_time",
            "entry_end_time",
            "entry_comment",
        ]

    def validate(self, data):
        action = self.context.get("action")

        # Validate based on action: "in" requires entry_start_time; "out" requires entry_end_time.
        if action == "in":
            if not data.get("entry_start_time"):
                raise serializers.ValidationError(
                    {
                        "entry_start_time": "This field is required for clock-in."
                    }
                )
            # Remove entry_end_time to ensure only start time is handled for "in" action.
            data.pop("entry_end_time", None)

        elif action == "out":
            if not data.get("entry_end_time"):
                raise serializers.ValidationError(
                    {"entry_end_time": "This field is required for clock-out."}
                )
            # Remove entry_start_time to ensure only end time is handled for "out" action.
            data.pop("entry_start_time", None)

        else:
            raise serializers.ValidationError(
                {
                    "action": "Invalid action specified. Use 'in' for clock-in or 'out' for clock-out."
                }
            )

        return data
