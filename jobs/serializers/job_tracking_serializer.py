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

        # Check if action is in the context and act accordingly
        if action == "in":
            if not data.get("entry_start_time"):
                raise serializers.ValidationError(
                    {
                        "entry_start_time": "This field is required for clock-in."
                    }
                )
        elif action == "out":
            # For clock-out action, ignore entry_start_time validation
            data.pop("entry_start_time", None)
        else:
            raise serializers.ValidationError(
                {"action": "Invalid action specified. Use 'in' or 'out'."}
            )

        return data
