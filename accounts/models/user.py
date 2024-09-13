"""
Custom User model with UUID primary key and additional fields for soft deletion.
"""
from __future__ import annotations

import uuid

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone


class SimpleUser(models.Model):
    """
    A simple user model with UUID as the primary key,
    full name, and PIN.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    pin = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def set_pin(self, pin):
        """
        Hashes and sets the PIN.
        """
        self.pin = make_password(pin)
        self.save()

    def check_pin(self, pin):
        """
        Checks if the provided PIN matches the stored hashed PIN.
        """
        return check_password(pin, self.pin)

    def soft_delete(self):
        """
        Marks the user as deleted by setting the `deleted_at` field to the current time.
        """
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return str(self.full_name)
