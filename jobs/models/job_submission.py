"""
This module defines the JobSubmission model for tracking submissions related to jobs.

The JobSubmission model includes a UUID-based primary key,
a comment, and foreign keys linking to the user who made the submission
and the job associated with the submission.
"""
from __future__ import annotations

import uuid

from django.db import models

from jobs.models import Job


class JobSubmission(models.Model):
    """
    Represents a submission made for a specific job.

    Attributes:
        id (UUIDField): A unique identifier for the job submission record.
        comment (TextField): A comment providing additional details about the submission.
        user (ForeignKey): A foreign key linking to the User model, representing
                            the user who made the submission.
        job (ForeignKey): A foreign key linking to the Job model,
                            representing the job associated with the submission.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField()
    user = models.ForeignKey(
        'accounts.SimpleUser', on_delete=models.CASCADE, related_name='job_submissions',
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE,
        related_name='submissions',
    )

    def __str__(self):
        return f"Submission ID {self.id}: Job ID {self.job} by User ID {self.user}"
