"""
This module imports the Devices and User models
for user and device management.

The Devices model is used for managing device
tokens with unique identifiers,
while the User model is used for managing user accounts
with UUID-based primary keys.
"""
from __future__ import annotations

from .user import SimpleUser
from .devices import Devices
# from .user import SimpleUser, CustomUser
from .user_devices import UserDevice
