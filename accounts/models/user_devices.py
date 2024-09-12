"""
This module defines the models for managing the
relationship between users and devices.

It includes:
- `UserDevice`: A model that links users to devices,
                capturing the relationship between them.
"""
from __future__ import annotations

from django.db import models

from accounts.models import Devices
from accounts.models import User


class UserDevice(models.Model):
    """
    This model represents the association between a user and a device.

    Attributes:
        user (ForeignKey):  A foreign key to the User model, indicating
                            the user associated with the device.
        device (ForeignKey): A foreign key to the Devices model, indicating
                            the device associated with the user.
        assigned_date (DateTimeField): The date and time when the
        device was assigned to the user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
