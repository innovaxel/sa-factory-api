"""
This module defines the Location model for managing geographical locations in Django.

The Location model includes a UUID-based primary key and a name. It represents a specific
geographical location with a unique identifier and a descriptive name.
"""
from __future__ import annotations

import uuid

from django.db import models


class Location(models.Model):
    """
    Represents a geographical location with a UUID as the primary key and a name.

    Attributes:
        id (UUIDField): The unique identifier for the location, automatically generated.
        name (CharField): The name of the location.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
