"""
time_calculator.py

This module contains the TimeCalculator class, which provides methods to 
calculate and format total time spent by users on specific jobs. It includes 
calculations for the current user's time spent in the current month and the 
total time spent by other users on a job.

Modules:
    - datetime: To handle time-related calculations.
    - django.utils.timezone: To access the current time and timezone-aware operations.
    - jobs.models: To access the Timesheet model for retrieving user timesheet entries.
"""

from datetime import timedelta
from django.utils import timezone
from jobs.models import Timesheet

class TimeCalculator:
    """
    A class to calculate and format total time spent by users on specific jobs.

    This class provides methods to calculate the time spent by the current user
    for the current month and the total time spent by other users on a job.
    """

    @staticmethod
    def format_total_time(total_time):
        """
        Formats a timedelta object into a string representation of total time.

        Args:
            total_time (timedelta): The total time to format.

        Returns:
            str: A string representing the total time in the format 'DD:HH:MM:SS' 
                 or 'HH:MM:SS'.
        """
        total_seconds = int(total_time.total_seconds())
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f"{days}:{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{hours:02}:{minutes:02}:{seconds:02}"

    @staticmethod
    def calculate_current_user_time(user, job_id):
        """
        Calculates the total time spent by the current user on a job 
        for the current month.

        Args:
            user (User): The user for whom to calculate time.
            job_id (int): The ID of the job.

        Returns:
            timedelta: The total time spent by the user on the job.
        """
        total_time = timedelta()
        timesheet_entries = Timesheet.objects.filter(job_id=job_id, user_id=user.id)
        sorted_entries = sorted(timesheet_entries, key=lambda entry: entry.timestamp)

        clock_in_time = None
        current_month = timezone.now().month
        current_year = timezone.now().year

        for entry in sorted_entries:
            timestamp = entry.timestamp

            if timestamp.month == current_month and timestamp.year == current_year:
                if entry.action.lower() == 'in':
                    clock_in_time = timestamp
                elif entry.action.lower() == 'out' and clock_in_time:
                    duration = timestamp - clock_in_time
                    total_time += duration
                    clock_in_time = None

        if clock_in_time:
            current_time = timezone.now()
            duration = current_time - clock_in_time
            total_time += duration

        return total_time

    @staticmethod
    def calculate_other_user_time(user, job_id):
        """
        Calculates the total time spent by another user on a job.

        Args:
            user (User): The user for whom to calculate time.
            job_id (int): The ID of the job.

        Returns:
            timedelta: The total time spent by the user on the job.
        """
        total_time = timedelta()
        timesheet_entries = Timesheet.objects.filter(job_id=job_id, user_id=user.id)
        sorted_entries = sorted(timesheet_entries, key=lambda entry: entry.timestamp)

        clock_in_time = None

        for entry in sorted_entries:
            timestamp = entry.timestamp

            if entry.action.lower() == 'in':
                clock_in_time = timestamp
            elif entry.action.lower() == 'out' and clock_in_time:
                duration = timestamp - clock_in_time
                total_time += duration
                clock_in_time = None

        if clock_in_time:
            current_time = timezone.now()
            duration = current_time - clock_in_time
            total_time += duration

        return total_time
