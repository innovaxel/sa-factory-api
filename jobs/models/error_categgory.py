"""
This module defines the Error Category model for managing categories in Django.

The Error Category model includes a UUID-based primary key, a name, and a code.
"""
from __future__ import annotations

import uuid

from django.db import models


class ErrorCategory(models.Model):
    """
    Represents a error category with a unique identifier, name, and code.

    Attributes:
        id (UUIDField): A unique identifier for the error category.
        name (CharField): The name of the error category.
        code (CharField): A code representing the error category.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Error Category: {self.name} (Code: {self.code})"
