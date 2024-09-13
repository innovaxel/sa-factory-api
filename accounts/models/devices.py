"""
This module defines the Devices model for managing device tokens in Django.

The Devices model includes a UUID-based primary key,
an API token, and timestamps for creation and updates.
"""
from __future__ import annotations

import uuid

from django.db import models


class Devices(models.Model):
    """
    Represents a device with a UUID as the primary key,
    an API token, and timestamps for creation and updates.

    Attributes:
        id (UUIDField): The unique identifier for the device, automatically generated.
        api_key (CharField): A unique token assigned to the device,
            with a maximum length of 10 characters.
        created_at (DateTimeField): The timestamp when the device was created,
            automatically set to the current time when the object is created.
        updated_at (DateTimeField): The timestamp when the device was last updated,
            automatically set to the current time whenever the object is saved.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.TextField(blank=False, null=False, unique=True)
    api_key = models.TextField(blank=False, null=False, unique=True)
    api_url = models.URLField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.device_id)
