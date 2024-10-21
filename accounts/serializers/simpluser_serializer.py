"""
This module contains serializers for the `SimpleUser` model.

The `SimpleUserSerializer` is responsible for converting `SimpleUser` model
instances into JSON and vice versa. It includes additional methods to compute
fields like `time_spent` and `pin_set`.
"""

from django.utils import timezone
from datetime import timedelta

from rest_framework import serializers
from jobs.models import Timesheet

from accounts.models import SimpleUser
from jobs.models import Chip


class SimpleUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the `SimpleUser` model.

    Converts `SimpleUser` model instances into JSON and vice versa.
    Includes the fields `id`, `full_name`, `role`, `time_spent`, and `pin_set`.
    """

    time_spent = serializers.SerializerMethodField()
    pin_set = serializers.SerializerMethodField()
    chip = serializers.SerializerMethodField()

    class Meta:
        """
        Metadata for the `SimpleUserSerializer`.

        Specifies the model to be serialized and the fields to include
        in the serialized representation.
        """

        model = SimpleUser
        fields = ['id', 'full_name', 'role', 'time_spent', 'chip', 'pin_set']

    def get_time_spent(self, obj):
        """
        Custom method to get the value for the `time_spent` field.
        Calculate the total time spent by the user on their current job.
        """
        return self._calculate_total_time(obj)

    def _calculate_total_time(self, user):
        """
        Calculate the total time a user has worked for their
        current job.
        """
        current_job = self._get_current_job(user)

        if not current_job:
            return '0 hours'

        if current_job.status != 'in_progress':
            return '0 hours'

        timesheet_entries = Timesheet.objects.filter(
            user_id=user.id,
            job_id=current_job.id,
        ).order_by('timestamp')

        if not timesheet_entries.exists():
            return '0 hours'

        total_time = timedelta()
        last_clock_in = None
        current_time = timezone.now()

        for entry in timesheet_entries:
            if entry.action == 'in':
                last_clock_in = entry.timestamp
            elif entry.action == 'out' and last_clock_in:
                if entry.timestamp > last_clock_in:
                    total_time += entry.timestamp - last_clock_in
                last_clock_in = None

        if last_clock_in:
            if last_clock_in > current_time:
                return '0 hours'
            total_time += current_time - last_clock_in

        total_seconds = int(total_time.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        if minutes > 0:
            total_hours = hours + minutes / 60
            return f"{total_hours:.1f} hours"

        return f"{hours} hours"

    def _get_current_job(self, user):
        """
        Custom method to retrieve the user's current job based
        on their most recent 'in' action.
        """
        current_timesheet_entry = (
            Timesheet.objects.filter(user_id=user.id, action='in')
            .order_by('-timestamp')
            .first()
        )

        if current_timesheet_entry:
            return current_timesheet_entry.job_id
        return None

    def get_pin_set(self, obj):
        """
        Custom method to get the value for the `pin_set` field.
        """
        return obj.pin is not None and obj.pin != ''

    def get_chip(self, obj):
        """
        Determine the chip based on time spent by querying the Chip model.
        """
        time_spent = self._calculate_total_time(obj)
        total_hours = float(time_spent.split()[0])
        if total_hours <= 1:
            chip_text = 'green'
        elif 1 <= total_hours < 3:
            chip_text = 'orange'
        else:
            chip_text = 'red'

        chip = Chip.objects.filter(text=chip_text).first()

        if chip:
            return {
                'id': str(chip.id),
                'color': chip.color,
                'text': chip.text,
                'icon': chip.icon,
            }
