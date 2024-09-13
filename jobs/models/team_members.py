"""
This module defines the TeamMember model for associating
users with worklists.

The TeamMember model includes a UUID-based primary key,
a user reference, and a worklist reference.
"""
from __future__ import annotations

import uuid

from django.db import models


class TeamMember(models.Model):
    """
    Represents a team member associated with a specific worklist.

    Attributes:
        id (UUIDField): A unique identifier for the team member record.
        user (ForeignKey): A foreign key linking to the User model.
        worklist (ForeignKey): A foreign key linking to the WorkList model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.SimpleUser', on_delete=models.CASCADE)
    worklist = models.ForeignKey('WorkList', on_delete=models.CASCADE)

    def __str__(self):
        return f"Team Member: User ID {self.user}, Worklist ID {self.worklist}"
