"""
This module defines the FactoryAppDevices model for managing device tokens in Django.

The FactoryAppDevices model includes a UUID-based primary key,
an API token, and timestamps for creation and updates.
"""

from __future__ import annotations

import uuid

from django.db import models


class FactoryAppDevices(models.Model):
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

    id = models.AutoField(primary_key=True)
    device_id = models.CharField(
        max_length=255, blank=False, null=False, unique=True
    )
    is_revoked = models.BooleanField(default=False)
    api_key = models.CharField(
        max_length=50, blank=False, null=False, unique=True
    )
    api_url = models.URLField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.device_id)

    class Meta:
        managed = True
        db_table = "HR_SYSTEM].[Factory_App_Devices"
