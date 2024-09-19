"""
This module defines the `JobLog` model for logging user interactions or
events related to jobs.

The `JobLog` model records entries for job-related activities, including
which user interacted with which job and when this interaction occurred.
This model is used to track job-related actions and can be useful for auditing
and tracking purposes.

"""

from __future__ import annotations

import uuid

from django.db import models

from jobs.models import Job


class JobLog(models.Model):
    """
    Represents a log entry for a job, recording user interactions or events.

    Attributes:
        id (UUIDField): A unique identifier for the job log entry.
        user (ForeignKey): A foreign key linking to the User model,
                            representing the user who interacted with the job.
        job (ForeignKey): A foreign key linking to the Job model,
                            representing the job related to this log entry.
        created_at (DateTimeField): The date and time when the log entry was created.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.SimpleUser', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
