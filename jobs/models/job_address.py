"""
This module defines the JobAddress model for storing address
and location information related to jobs.
The JobAddress model includes a UUID-based primary key, address details,
and separate fields for latitude and longitude.
"""
from __future__ import annotations

import uuid

from django.db import models


class JobAddress(models.Model):
    """
    Represents an address and its geographic coordinates associated with a specific job.

    Attributes:
        id (UUIDField): A unique identifier for the job address record.
        address (CharField): The street address for the job.
        latitude (DecimalField): The latitude coordinate for the job address.
        longitude (DecimalField): The longitude coordinate for the job address.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"Job Address ID {self.id}: {self.address}, \
            Latitude {self.latitude}, Longitude {self.longitude}"
