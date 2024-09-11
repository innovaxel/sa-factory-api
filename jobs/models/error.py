"""
This module defines the Error model for logging errors associated with jobs.

The Error model includes a UUID-based primary key, a reference
to the subcategory of the error, a comment, and foreign keys
linking to the user who reported the error and the job associated with the error.
"""
from __future__ import annotations

import uuid

from django.db import models

from accounts.models import User
from jobs.models import ErrorSubCategory
from jobs.models import Job


class Error(models.Model):
    """
    Represents an error logged in relation to a specific job.

    Attributes:
        id (UUIDField): A unique identifier for the error record.
        errorsubcategory (ForeignKey): A foreign key linking to the SubCategory model,
                                        representing the category of the error.
        comment (TextField): A comment providing additional details about the error.
        user (ForeignKey): A foreign key linking to the User model, representing
                            the user who reported the error.
        job (ForeignKey): A foreign key linking to the Job model, representing the
                            job associated with the error.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    errorsubcategory = models.ForeignKey(
        ErrorSubCategory,
        on_delete=models.CASCADE, related_name='errors',
    )
    comment = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reported_errors',
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='errors',
    )

    def __str__(self):
        return f"Error ID {self.id}: {self.errorsubcategory.name}\
              - Reported by User ID {self.user} for Job ID {self.job}"
