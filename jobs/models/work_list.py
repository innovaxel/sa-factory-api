"""
This module defines the WorkList model for managing tasks or items
associated with geographical locations in Django.

The WorkList model includes a UUID-based primary key,
a title, and a foreign key reference to a Location.
"""
from __future__ import annotations

import uuid

from django.db import models

from jobs.models.location import Location


class WorkList(models.Model):
    """
    Represents a worklist item associated with a specific location,
    with a UUID as the primary key and a title.

    Attributes:
        id (UUIDField): The unique identifier for the worklist item,
        automatically generated.
        title (CharField): The title of the worklist item.
        location (ForeignKey): A reference to the Location this worklist
        item is associated with.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='worklists',
    )

    def __str__(self):
        return str(self.title)
