"""
ViewSet for managing `WorkList` items.

This module defines the `WorkListViewSet` class, which provides
CRUD operations for `WorkList` instances.
The `WorkListViewSet` class includes methods for listing,
creating, retrieving, updating, and deleting
`WorkList` items, with custom response formats for each operation.

- `create`: Creates a new `WorkList` item with custom response format.
            Handles validation and error cases.
- `update`: Updates an existing `WorkList` item with custom response format.
            Handles validation and partial updates.
- `destroy`: Deletes a specific `WorkList` item with custom response format.
            Returns success or error responses.
- `list`: Lists all `WorkList` items with custom response format. Handles errors
            and returns a success response.
- `retrieve`: Retrieves a specific `WorkList` item by ID with custom response
            format. Handles errors and returns a success response.
"""
from __future__ import annotations

import logging

from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from common.device_validator import DeviceValidator
from accounts.permission import IsAdminOrReadOnly

from jobs.models import WorkList
from jobs.serializers import WorkListSerializer

logger = logging.getLogger('jobs')


class WorkListViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing `WorkList` items.

    Provides CRUD operations for `WorkList` instances, including list,
    create, retrieve, update, and delete operations.
    """
    queryset = WorkList.objects.all()
    serializer_class = WorkListSerializer

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
        Creates a new `WorkList` item.

        Handles validation and returns success or error responses.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)

                logger.info('WorkList item created successfully.')
                return Response(
                    {
                        'message': 'WorkList item created successfully.',
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
            logger.error('Validation error.')
            return Response(
                {
                    'message': 'Validation error.',
                    'data': e.detail,
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error('Error creating WorkList item: %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        """
        Updates an existing `WorkList` item.

        Handles partial updates if specified and returns success or
        error responses.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            if serializer.is_valid():
                self.perform_update(serializer)

                logger.info('WorkList item updated successfully.')
                return Response(
                    {
                        'message': 'WorkList item updated successfully.',
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
            logger.error('Validation error.')
            return Response(
                {
                    'message': 'Validation error.',
                    'data': e.detail,
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error('Error updating WorkList item: %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Deletes an existing `WorkList` item.

        Returns success or error responses based on the result of the
        deletion operation.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)

            logger.info('WorkList item deleted successfully.')
            return Response(
                {
                    'message': 'WorkList item deleted successfully.',
                }, status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            logger.error('Error deleting WorkList item: %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request, *args, **kwargs):
        """
        List all `WorkList` items with a custom response format.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)

            logger.info(
                'WorkList items retrieved successfully. Count=%s', len(serializer.data),
            )
            return Response(
                {
                    'message': 'WorkList items retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error('An error occurred. %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific `WorkList` item by ID with a custom response format.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            logger.info('WorkList item retrieved successfully.')
            return Response(
                {
                    'message': 'WorkList item retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error('An error occurred. %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
