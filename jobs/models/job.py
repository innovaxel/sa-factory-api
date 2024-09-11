"""
This module defines the Job model for the application.
"""
from __future__ import annotations

import uuid

from django.db import models

from jobs.models.chip import Chip
from jobs.models.customer import Customer
from jobs.models.job_address import JobAddress
from jobs.models.work_list import WorkList


class Job(models.Model):
    """
    Represents a job in the application.

    Attributes:
        id (UUIDField): A unique identifier for the job.
        name (CharField): The name of the job.
        number (IntegerField): A number associated with the job.
        customerid (ForeignKey): A foreign key linking to the Customer model.
        worklistid (ForeignKey): A foreign key linking to the WorkList model.
        chip (CharField): An optional field for additional chip information.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    address_id = models.ForeignKey(JobAddress, on_delete=models.CASCADE)
    customerid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    worklistid = models.ForeignKey(WorkList, on_delete=models.CASCADE)
    chip = models.ForeignKey(Chip, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
