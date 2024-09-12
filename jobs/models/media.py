"""
This module defines the Media model for managing media resources in Django.

The Media model includes a UUID-based primary key,
a resource identifier, and a file path for the media image.
"""
from __future__ import annotations

import uuid

from django.db import models


class Media(models.Model):
    """
    Represents a media resource associated with a specific resource identifier.

    Attributes:
        id (UUIDField): A unique identifier for the media record.
        resource_id (CharField): An identifier for the resource associated with the media.
        image (ImageField): The file path for the media image.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_id = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='media/images/')

    def __str__(self):
        return f"Media ID {self.id}: Resource ID \
            {self.resource_id}, Image Path {self.image}"
