"""
This module provides the `DeviceValidator` class for validating device IDs.

The `DeviceValidator` class is used to verify if a given device ID is valid and exists in the `Devices` model. It is primarily used to ensure that API requests are coming from authorized devices.

Classes:
    - `DeviceValidator`: Handles validation of device IDs.

Usage:
    - Instantiate the `DeviceValidator` with a device ID.
    - Call the `validate` method to check the validity of the device ID.
      - Returns a structured `Response` if the device ID is invalid or missing.
      - Returns `None` if the device ID is valid.
"""

import logging
from rest_framework import status
from rest_framework.response import Response
from accounts.models import Devices

logger = logging.getLogger('django')

class DeviceValidator:
    """
    Class to validate device IDs for API access.
    """

    def __init__(self, device_id: str):
        """
        Initialize with the device ID to be validated.

        Args:
            device_id (str): The device ID to validate.
        """
        self.device_id = device_id

    def validate(self):
        """
        Validates the device ID.

        Returns:
            Response: A structured response if the device ID is valid.
            Raises:
                PermissionDenied: If the device ID is invalid or missing.
        """
        if not self.device_id:
            logger.error("Device ID is not provided.")
            return Response(
                {"message": "Device ID is not provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not Devices.objects.filter(device_id=self.device_id).exists():
            logger.error("Invalid device ID.")
            return Response(
                {"message": "Invalid device ID."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return None
