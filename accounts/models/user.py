"""
Custom User model with UUID primary key and additional fields for soft deletion.
"""
from __future__ import annotations

import uuid

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model with a UUID primary key, username,
    pin, and timestamps for management.

    Attributes:
        id (UUIDField): The unique identifier for the user, automatically generated.
        username (CharField): The username of the user, must be unique
                with a maximum length of 10 characters.
        pin (CharField): The hashed PIN or password for the user,
                with a maximum length of 128 characters.
        created_at (DateTimeField): The timestamp when the user was created,
                                    automatically set to the current time.
        updated_at (DateTimeField): The timestamp when the user was last updated,
                                    automatically set to the current time.
        deleted_at (DateTimeField): The timestamp when the user was soft-deleted,
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True)
    pin = models.CharField(max_length=200)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.username)
