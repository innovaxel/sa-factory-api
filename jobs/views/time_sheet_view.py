"""
ViewSet for managing `Timesheet` entries.

This module defines the `TimesheetViewSet` class, which provides operations
for managing timesheet entries. The `TimesheetViewSet` class includes methods
for creating new timesheet entries and calculating the total time spent by
a user today.

- `create`: Handles the creation of new `Timesheet` entries with validation and
             appropriate responses based on the action (`in` or `out`).
- `_calculate_total_time_today`: Helper method to compute the total time spent
                                  today by a specific user.
"""

from datetime import datetime, time, timedelta
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.utils.timezone import make_aware, now
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from jobs.models import Timesheet, Job, JobLog

from accounts.permission import IsAdminOnly
from common.device_validator import DeviceValidator

from jobs.serializers import TimesheetSerializer, UserWorkTimeRequestSerializer


class TimesheetViewSet(viewsets.ViewSet):
    """
    ViewSet for managing timesheet entries.

    Allows authenticated users to clock in or out, tracks time spent,
    and returns the total time spent today. Handles device validation
    before processing timesheet actions.
    """
    permission_classes = [IsAuthenticated]

    def _calculate_total_time_today(self, user, current_time=None):
        """
        Calculate the total time a user has worked today.
        """
        if current_time is None:
            current_time = now()

        today_start = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        timesheet_entries = Timesheet.objects.filter(
            user_id=user.id, timestamp__gte=today_start,
        ).order_by('timestamp')

        total_time = timedelta()
        last_clock_in = None

        for entry in timesheet_entries:
            if entry.action == 'in':
                last_clock_in = entry.timestamp
            elif entry.action == 'out' and last_clock_in:
                total_time += entry.timestamp - last_clock_in
                last_clock_in = None

        if last_clock_in:
            total_time += current_time - last_clock_in

        total_seconds = int(total_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours}:{minutes:02}:{seconds:02}"

    def create(self, request):
        """
        Handle clock-in or clock-out actions for the authenticated user.
        Validates the device and ensures appropriate actions are taken.
        Returns the total time spent today.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        serializer = TimesheetSerializer(data=request.data)
        if serializer.is_valid():
            action = serializer.validated_data['action']
            job_id = serializer.validated_data['job'].id
            user = request.user
            timestamp = request.data.get('timestamp')

            if timestamp:
                current_time = make_aware(parse_datetime(timestamp))
            else:
                current_time = now()

            today_start = current_time.replace(
                hour=0, minute=0, second=0, microsecond=0,
            )
            nine_am_today = current_time.replace(
                hour=9, minute=0, second=0, microsecond=0,
            )

            job = Job.objects.get(id=job_id)
            job_log_exists = JobLog.objects.filter(user=user, job=job.id).exists()

            if not job_log_exists:
                JobLog.objects.create(user=user, job=job)

            last_entry = Timesheet.objects.filter(
                user_id=user.id, timestamp__gte=today_start,
            ).order_by('-timestamp').first()

            if action == 'out':
                if last_entry and last_entry.action == 'in':
                    Timesheet.objects.create(
                        user_id=user,
                        job_id=job,
                        action=action,
                        timestamp=current_time,
                    )
                    total_time_today = self._calculate_total_time_today(
                        user,
                        current_time=current_time,
                    )
                    return Response(
                        {
                            'message': 'Clocked out successfully.',
                            'data': {
                                'time_spent': str(total_time_today),
                            },
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    last_entry = Timesheet.objects.filter(
                        user_id=user.id,
                    ).order_by('-timestamp').first()
                    if last_entry and last_entry.action == 'in':
                        Timesheet.objects.create(
                            user_id=user,
                            job_id=job,
                            action=action,
                            timestamp=current_time,
                        )
                        clock_in_time = max(last_entry.timestamp, nine_am_today)
                        total_time_today = current_time - clock_in_time
                        return Response(
                            {
                                'message': 'Clocked out successfully.',
                                'data': {
                                    'time_spent': str(total_time_today),
                                },
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            {
                                'message': 'Cannot clock out without clocking in.',
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

            elif action == 'in':
                if last_entry and last_entry.action == 'in':
                    return Response(
                        {
                            'message': 'Cannot clock in again \
                                without clocking out first.',
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                Timesheet.objects.create(
                    user_id=user,
                    job_id=job,
                    action=action,
                    timestamp=current_time,
                )
                total_time_today = self._calculate_total_time_today(
                    user,
                    current_time=current_time,
                )
                return Response(
                    {
                        'message': 'Clocked in successfully.',
                        'data': {
                            'time_spent': str(total_time_today),
                        },
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        'message': 'Invalid action.',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {
                'message': 'Invalid data provided.',
                'errors': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserWorkTimeView(APIView):
    """
    API view to calculate the total time a user worked on a specific day and job.
    """
    permission_classes = [IsAdminOnly]

    def post(self, request):
        """
        Calculate and return the total work time for the specified user, date, and job.

        This method processes the input data, filters the timesheet entries based on
        the provided user ID, date, and optionally job ID, and calculates the total
        work time. It considers the standard working hours (9 AM to 5 PM) and
        adjusts the calculation based on clock-in and clock-out entries.

        Args:
            request (Request): The HTTP request containing
            `user_id`, `date`, and optionally `job_id`.

        Returns:
            Response: A response containing the total work time
            spent by the user on the specified day and job.
        """

        serializer = UserWorkTimeRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'message': 'Invalid input data',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = serializer.validated_data['user_id']
        date = serializer.validated_data['date']
        job_id = serializer.validated_data.get('job_id')

        shift_start_time = make_aware(datetime.combine(date, time(9, 0)))
        shift_end_time = make_aware(datetime.combine(date, time(17, 0)))

        timesheet_filter = {
            'user_id': user_id,
            'timestamp__date': date,
        }

        if job_id:
            timesheet_filter['job_id'] = job_id

        timesheet_entries = Timesheet.objects.filter(
            **timesheet_filter,
        ).order_by('timestamp')

        if not timesheet_entries.exists():
            return Response(
                {
                    'message': 'Total work time for the specified day and job.',
                    'data': {
                        'total_time_spent': str(timedelta(hours=8)),
                    },
                },
                status=status.HTTP_200_OK,
            )

        total_time = timedelta()
        last_clock_in = None
        only_clock_out = None

        for entry in timesheet_entries:
            if entry.action == 'in':
                last_clock_in = entry.timestamp
            elif entry.action == 'out':
                if last_clock_in:
                    total_time += entry.timestamp - last_clock_in
                    last_clock_in = None
                else:
                    only_clock_out = entry.timestamp

        if last_clock_in:
            total_time += min(shift_end_time, timezone.now()) - last_clock_in

        if only_clock_out:
            total_time += only_clock_out - shift_start_time

        return Response(
            {
                'message': 'Total work time for the specified day and job.',
                'data': {
                    'total_time_spent': str(total_time),
                },
            },
            status=status.HTTP_200_OK,
        )
