"""
This module defines the Chip model for managing UI components like chips in Django.

The Chip model includes a UUID-based primary key, a color, text, and an icon.
"""
from __future__ import annotations

import uuid

from django.db import models


class Chip(models.Model):
    """
    Represents a chip with a UUID as the primary key, color, text, and icon.

    Attributes:
        id (UUIDField): The unique identifier for the chip, automatically generated.
        color (CharField): The color associated with the chip.
        text (CharField): The text displayed on the chip.
        icon (CharField): An optional icon identifier or path for the chip.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    color = models.CharField(max_length=50)
    text = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.text} ({self.color})"
