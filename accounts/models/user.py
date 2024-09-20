"""
Custom User model with UUID primary key and additional fields for soft deletion.
"""
from __future__ import annotations

import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.utils import timezone


class SimpleUser(AbstractUser):
    """
    A simple user model with UUID as the primary key,
    full name, and PIN.
    """

    USER_ROLE_CHOICES = [
        ('Apprentice', 'Apprentice'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    pin = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(
        max_length=100, choices=USER_ROLE_CHOICES,
        default='Apprentice',
    )
    workilist_id = models.ForeignKey(
        'jobs.WorkList', on_delete=models.CASCADE,
        blank=True, null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.username:
            base_username = self.full_name.replace(' ', '').lower() \
                if self.full_name else 'user'
            username = base_username
            suffix = 1

            while SimpleUser.objects.filter(username=username).exists():
                username = f"{base_username}-{suffix}"
                suffix += 1

            self.username = username

        if self.pin:
            self.password = make_password(self.pin)

        super().save(*args, **kwargs)

    def soft_delete(self):
        """
        Marks the user as deleted by setting the `deleted_at`
        field to the current time.
        """
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return str(self.username)
