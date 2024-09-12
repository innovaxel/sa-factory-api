"""
This module imports the Devices and User models
for user and device management.

The Devices model is used for managing device
tokens with unique identifiers,
while the User model is used for managing user accounts
with UUID-based primary keys.
"""
from __future__ import annotations

from .devices import Devices
from .user import User
from .user_devices import UserDevice