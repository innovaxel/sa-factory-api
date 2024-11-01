from datetime import timedelta
import random
from rest_framework import serializers
from accounts.models import HumanResource
from jobs.models.job_tracking import JobTrackingEntry


class HumanResourceSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """

    pin_set = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    time_spent = serializers.SerializerMethodField()
    chip = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = HumanResource
        fields = [
            "id",
            "pin",
            "full_name",
            "role",
            "pin_set",
            "time_spent",
            "chip",
        ]

    id = serializers.CharField(source="hr_guid")
    pin = serializers.CharField(source="hr_pin")

    def get_role(self, obj):
        """Return the role for the human resource."""
        return "Apprentice"

    def get_pin_set(self, obj):
        """Custom method to get the value for the `pin_set` field."""
        return obj.hr_pin is not None and obj.hr_pin != ""

    def get_full_name(self, obj):
        """Custom method to get the full name by concatenating first and last names from Contact."""
        contact = obj.contact_id
        if contact:
            return f"{contact.contact_first_name} {contact.contact_last_name or ''}".strip()
        return ""

    def get_time_spent(self, obj):
        """Calculate and return the total time spent on the last job for this HR resource."""
        task_gid = "your_task_gid_here"
        total_time = self.calculate_total_time_for_last_job(
            obj.hr_id, task_gid
        )
        return total_time

    def get_chip(self, obj):
        """Determine chip information based on time spent."""
        task_gid = "your_task_gid_here"
        total_time = self.calculate_total_time_for_last_job(
            obj.hr_id, task_gid
        )

        chip = {
            "id": str(random.randint(10000, 99999)),
            "color": self.get_chip_color(total_time),
            "text": self.get_chip_text(total_time),
            "icon": self.get_chip_icon(total_time),
        }
        return chip

    def get_chip_color(self, total_time):
        """Determine the chip color based on total time."""
        hours = total_time.total_seconds() / 3600
        if hours < 1:
            return "#4CAF50"
        elif 1 <= hours < 3:
            return "#FFA500"
        else:
            return "#F95454"

    def get_chip_text(self, total_time):
        """Return text for the chip based on total time."""
        hours = total_time.total_seconds() / 3600
        if hours < 1:
            return "Under 1 hour"
        elif 1 <= hours < 3:
            return "1-3 hours"
        else:
            return "3+ hours"

    def get_chip_icon(self, total_time):
        """Return an icon for the chip based on total time."""
        hours = total_time.total_seconds() / 3600
        if hours < 1:
            return "icon_green"
        elif 1 <= hours < 3:
            return "icon_orange"
        else:
            return "icon_red"

    def calculate_total_time_for_last_job(self, hr_id, task_gid):
        """Calculate the total time spent on the last job for the given HR resource."""
        last_entry = (
            JobTrackingEntry.objects.filter(
                entry_task_gid=task_gid,
                entry_hr=hr_id,
                entry_end_time__isnull=False,
            )
            .order_by("-entry_end_time")
            .first()
        )

        if last_entry:
            total_duration = (
                last_entry.entry_end_time - last_entry.entry_start_time
            )
            return total_duration

        return timedelta()
