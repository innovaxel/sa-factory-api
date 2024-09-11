"""
This module defines the SubCategory model for managing subcategories in Django.

The SubCategory model includes a UUID-based primary key,
a name, a code, and a reference to a parent category.
"""
from __future__ import annotations

import uuid

from django.db import models

from jobs.models import ErrorCategory


class ErrorSubCategory(models.Model):
    """
    Represents a subcategory associated with a specific category.

    Attributes:
        id (UUIDField): A unique identifier for the subcategory.
        name (CharField): The name of the subcategory.
        code (CharField): A code representing the subcategory.
        category (ForeignKey): A foreign key linking to the Category model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    error_category = models.ForeignKey(
        ErrorCategory,
        on_delete=models.CASCADE, related_name='subcategories',
    )

    def __str__(self):
        return f"ErrorSubCategory: {self.name}\
              (Code: {self.code}), Error Category: {self.error_category.name}"
