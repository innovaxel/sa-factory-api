"""
This module defines the Customer model for managing customer information in Django.

The Customer model includes a UUID-based primary key and a name.
"""
from __future__ import annotations

import uuid

from django.db import models


class Customer(models.Model):
    """
    Represents a customer with a UUID as the primary key and a name.

    Attributes:
        id (UUIDField): The unique identifier for the customer, automatically generated.
        name (CharField): The name of the customer.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
