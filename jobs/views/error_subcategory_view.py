"""
ViewSet for the `ErrorSubCategory` model.

This module defines the `ErrorSubCategoryViewSet` class,
which provides CRUD operations for
`ErrorSubCategory` instances. The `ErrorSubCategoryViewSet`
class includes methods for listing,
creating, retrieving, updating, and deleting `ErrorSubCategory`
instances, with custom response
formats for each operation.

- `create`: Handles creation of new `ErrorSubCategory`
            instances with a custom response format.
- `update`: Updates an existing `ErrorSubCategory` instance with a
            custom response format.
- `destroy`: Deletes a specific `ErrorSubCategory` instance with a
            custom response format.
- `list`: Retrieves and lists all `ErrorSubCategory` instances with a
            custom response format.
- `retrieve`: Retrieves and returns a specific `ErrorSubCategory`
                instance by ID with a custom response format.
"""
from __future__ import annotations

import logging

from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from common.device_validator import DeviceValidator
from accounts.permission import IsAdminOrReadOnly

from jobs.models import ErrorSubCategory
from jobs.serializers import ErrorSubCategorySerializer

logger = logging.getLogger('jobs')


class ErrorSubCategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ErrorSubCategory instances.

    Provides methods for creating, listing, retrieving, updating,
    and deleting ErrorSubCategory instances.
    """
    queryset = ErrorSubCategory.objects.all()
    serializer_class = ErrorSubCategorySerializer

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
        Create a new `ErrorSubCategory` instance with custom response format.

        Validates the incoming data, creates a new ErrorSubCategory
        instance, and returns a success response.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                headers = self.get_success_headers(serializer.data)

                logger.info('ErrorSubCategory created successfully.')
                return Response(
                    {
                        'message': 'ErrorSubCategory created successfully.',
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
            logger.error('An error occurred. %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request, *args, **kwargs):
        """
        List all `ErrorSubCategory` instances with custom response format.

        Retrieves all ErrorSubCategory instances, serializes them,
        and returns a success response.
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
                'ErrorSubCategory items retrieved successfully. Count: %s',
                len(serializer.data),
            )
            return Response(
                {
                    'message': 'ErrorSubCategory items retrieved successfully.',
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
        Retrieve a specific `ErrorSubCategory` instance by ID with
        custom response format.

        Retrieves a single ErrorSubCategory instance, serializes it,
        and returns a success response.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            logger.info('ErrorSubCategory item retrieved successfully.')
            return Response(
                {
                    'message': 'ErrorSubCategory item retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except self.get_object().DoesNotExist:
            logger.error('ErrorSubCategory item not found.')
            return Response(
                {
                    'message': 'ErrorSubCategory item not found.',
                }, status=status.HTTP_404_NOT_FOUND,
            )
        except PermissionDenied:
            logger.error('Permission denied.')
            return Response(
                {
                    'message': 'Permission denied.',
                }, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            logger.error('An error occurred. %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        """
        Update a specific `ErrorSubCategory` instance with custom response format.

        Validates and updates an existing ErrorSubCategory instance,
        then returns a success response.
        """
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)

                logger.info('ErrorSubCategory updated successfully.')
                return Response(
                    {
                        'message': 'ErrorSubCategory updated successfully.',
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
            logger.error('An error occurred. %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific `ErrorSubCategory` instance with custom response format.

        Deletes an existing ErrorSubCategory instance and returns a success response.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)

            logger.info('ErrorSubCategory deleted successfully.')
            return Response(
                {
                    'message': 'ErrorSubCategory deleted successfully.',
                }, status=status.HTTP_204_NO_CONTENT,
            )
        except PermissionDenied:
            logger.error('Permission denied for deletion.')
            return Response(
                {
                    'message': 'Permission denied.',
                }, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            logger.error('An error occurred. %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
