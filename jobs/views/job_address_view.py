"""
ViewSet for managing `JobAddress` instances.

This module defines the `JobAddressViewSet` class, which provides CRUD
operations for `JobAddress`
instances. The `JobAddressViewSet` class includes methods for listing,
creating, retrieving, updating,
and deleting `JobAddress` instances, with custom response
formats for each operation. It supports
handling permissions for simple users and admins.

- `create`: Handles the creation of new `JobAddress` instances with a
custom response format.
- `list`: Lists all `JobAddress` instances with a custom response format.
- `retrieve`: Retrieves and returns a specific `JobAddress`
                instance by ID with a custom response format.
- `update`: Updates an existing `JobAddress` instance with a custom response format.
- `destroy`: Deletes a specific `JobAddress` instance with a custom response format.
"""
from __future__ import annotations

import logging

from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from common.device_validator import DeviceValidator
from accounts.permission import IsAdminOrReadOnly

from jobs.models import JobAddress
from jobs.serializers import JobAddressSerializer

logger = logging.getLogger('jobs')


class JobAddressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Job Address. Allows
    listing, creating, and modifying, and deleting Job Address.
    Job Address with different permissions for simple users and admins.
    """

    queryset = JobAddress.objects.all()
    serializer_class = JobAddressSerializer

    def get_permissions(self):
        """
        Return the permission classes based on the action.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminOrReadOnly()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Create a new `JobAddress` item with custom response format.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)

                logger.info('JobAddress created successfully.')
                return Response(
                    {
                        'message': 'JobAddress created successfully.',
                        'data': serializer.data,
                    }, status=status.HTTP_201_CREATED, headers=headers,
                )
            else:
                logger.error('Invalid data.')
                return Response(
                    {
                        'message': 'Invalid data.',
                        'errors': serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST,
                )
        except ValidationError as e:
            logger.error('Validation error. %s', e.detail)
            return Response(
                {
                    'message': 'Validation error.',
                    'data': e.detail,
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error('Error creating JobAddress. %s', str(e))
            return Response(
                {
                    'message': str(e),
                    'data': None,
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request, *args, **kwargs):
        """
        List all `JobAddress` items with custom response format.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)

            logger.info('JobAddress items retrieved successfully.')
            return Response(
                {
                    'message': 'JobAddress items retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error('Error retrieving JobAddress items. %s', str(e))
            return Response(
                {
                    'message': str(e),
                    'data': None,
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific `JobAddress` item by ID with custom response format.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            logger.info('JobAddress item retrieved successfully.')
            return Response(
                {
                    'message': 'JobAddress item retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except self.get_object().DoesNotExist:
            logger.error('JobAddress item not found.')
            return Response(
                {
                    'message': 'JobAddress item not found.',
                    'data': None,
                }, status=status.HTTP_404_NOT_FOUND,
            )
        except PermissionDenied:
            logger.error('Permission denied.')
            return Response(
                {
                    'message': 'Permission denied.',
                    'data': None,
                }, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            logger.error('Error retrieving JobAddress item. %s', str(e))
            return Response(
                {
                    'message': str(e),
                    'data': None,
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        """
        Update a specific `JobAddress` item with custom response format.
        """
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)
                logger.info('JobAddress updated successfully.')
                return Response(
                    {
                        'message': 'JobAddress updated successfully.',
                        'data': serializer.data,
                    }, status=status.HTTP_200_OK,
                )
            else:
                logger.error('Invalid data.')
                return Response(
                    {
                        'message': 'Invalid data.',
                        'errors': serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST,
                )
        except ValidationError as e:
            logger.error('Validation error. %s', e.detail)
            return Response(
                {
                    'message': 'Validation error.',
                    'data': e.detail,
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error('Error updating JobAddress. %s', str(e))
            return Response(
                {
                    'message': str(e),
                    'data': None,
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific `JobAddress` item with custom response format.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)

            logger.info('JobAddress deleted successfully.')
            return Response(
                {
                    'message': 'JobAddress deleted successfully.',
                    'data': None,
                }, status=status.HTTP_204_NO_CONTENT,
            )
        except PermissionDenied:
            logger.error('Permission denied.')
            return Response(
                {
                    'message': 'Permission denied.',
                    'data': None,
                }, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            logger.error('Error deleting JobAddress. %s', str(e))
            return Response(
                {
                    'message': str(e),
                    'data': None,
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
