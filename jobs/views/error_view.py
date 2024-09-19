"""
ViewSet for managing `Error` entries.

This module defines the `ErrorViewSet` class, which provides operations
for managing error entries in the system. The `ErrorViewSet` class includes methods
for listing, retrieving, creating, updating, and deleting errors. It also handles
media file uploads associated with errors.

- `perform_create`: Custom method to assign the logged-in user to the `Error`
                    and handle media uploads.
- `create`: Handles the creation of new `Error` entries with validation and
            appropriate responses based on the action. Logs the creation of
            errors and associates them with the authenticated user.
- `list`: Retrieves a list of all `Error` entries along with their related media.
- `retrieve`: Retrieves a specific `Error` entry along with its related media by ID.
"""
from __future__ import annotations

import logging

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.device_validator import DeviceValidator
from jobs.models import Error, Media
from jobs.serializers import ErrorSerializer, MediaSerializer

logger = logging.getLogger('jobs')


class ErrorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, creating, updating, and deleting errors.
    Only authenticated users can access this endpoint.
    """
    queryset = Error.objects.all()
    serializer_class = ErrorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom method to assign the logged-in user to the Error
        and handle media uploads.
        """
        error = serializer.save(user=self.request.user)

        media_files = self.request.FILES.getlist('media')
        for media in media_files:
            Media.objects.create(resource_id=error.id, image=media)

    def create(self, request, *args, **kwargs):
        """
        Custom create method for Error records.
        Associates the error with the authenticated user and adds logging.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        request_data = request.data.copy()
        user = request.user
        request_data['user'] = user.id

        serializer = self.get_serializer(data=request_data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.info(
                'Error created successfully for Job ID: %s by User ID: %s',
                request_data['job_id'], user.id,
            )
            return Response(
                {
                    'message': 'Error submitted successfully.',
                }, status=status.HTTP_201_CREATED,
            )
        else:
            logger.error('Error creation failed: %s', serializer.errors)
            return Response(
                {
                    'message': 'Error creation failed.',
                    'errors': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST,
            )

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all errors along with their related media.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        errors = Error.objects.all()
        data = []
        for error in errors:
            error_data = ErrorSerializer(error).data

            media_files = Media.objects.filter(resource_id=error.id)
            media_data = MediaSerializer(media_files, many=True).data

            error_data['media'] = media_data
            data.append(error_data)

        return Response(
            {
                'message': 'List of all errors with media files.',
                'data': data,
            }, status=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific error along with its related media by ID.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        error = self.get_object()

        error_data = ErrorSerializer(error).data

        media_files = Media.objects.filter(resource_id=error.id)
        media_data = MediaSerializer(media_files, many=True).data

        error_data['media'] = media_data

        return Response(
            {
                'message': 'Error with media files retrieved successfully.',
                'data': error_data,
            }, status=status.HTTP_200_OK,
        )
