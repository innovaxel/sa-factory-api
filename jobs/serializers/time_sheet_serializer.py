"""
Serializer module for `Timesheet` model.

This module defines the `TimesheetSerializer` class, which serializes
and deserializes instances of the `Timesheet` model.
"""
from __future__ import annotations

from rest_framework import serializers
from jobs.models import Timesheet, Job


class TimesheetSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Timesheet` model.

    Fields:
        user_id: The user related to the timesheet (read-only).
        job_id: The job related to the timesheet.
        action: The action (clock-in/clock-out).
        timestamp: The time of the action.
    """
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(), source='job')

    class Meta:
        """
        Meta class specifying the model and fields to include.
        """
        model = Timesheet
        fields = ['id', 'user_id', 'job_id', 'action', 'timestamp']


class UserWorkTimeRequestSerializer(serializers.Serializer):
    """
    Serializer for user work time request data.

    This serializer validates and processes the input data required
    to calculate the work time for a user on a specific job for a given date.

    Fields:
        user_id (UUIDField): The UUID of the user for whom work time is being requested.
        date (DateField): The date for which the work time is being calculated.
        job_id (UUIDField): The UUID of the job for which work time is being requested.
    """
    user_id = serializers.UUIDField()
    date = serializers.DateField()
    job_id = serializers.UUIDField()
