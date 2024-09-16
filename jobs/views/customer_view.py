"""
ViewSet for the `Customer` model.

This module defines the `CustomerViewSet` class, which provides CRUD operations for
`Customer` instances. The `CustomerViewSet` class includes methods for creating, listing,
retrieving, updating, and deleting `Customer` instances, with custom response formats
for each operation.

- `create`: Handles creation of new `Customer` instances with custom response format.
- `list`: Retrieves and lists all `Customer` instances with custom response format.
- `retrieve`: Retrieves a single `Customer` instance by
                its ID with custom response format.
- `update`: Updates an existing `Customer` instance with custom response format.
- `destroy`: Deletes a specific `Customer` instance with custom response format.
"""
from __future__ import annotations

import logging

from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from jobs.models import Customer
from jobs.serializers import CustomerSerializer

logger = logging.getLogger('jobs')


class CustomerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Customer instances.

    Provides methods for creating, listing, retrieving, updating, and deleting customers.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new `Customer` item with custom response format.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                logger.info('Customer created successfully.')
                return Response(
                    {
                        'status_code': status.HTTP_201_CREATED,
                        'message': 'Customer created successfully.',
                        'data': serializer.data,
                    }, status=status.HTTP_201_CREATED, headers=headers,
                )
            else:
                logger.warning(
                    'Invalid data for Customer creation: %s',
                    serializer.errors,
                )
                return Response(
                    {
                        'status_code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid data.',
                        'data': serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST,
                )
        except ValidationError as e:
            logger.error('Validation error during Customer creation: %s', e.detail)
            return Response(
                {
                    'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'message': 'Validation error.',
                    'data': e.detail,
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error('Unexpected error during Customer creation: %s', str(e))
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request, *args, **kwargs):
        """
        List all `Customer` items with custom response format.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)

            logger.info(
                'Customer items retrieved successfully. Count: %d',
                len(serializer.data),
            )
            return Response(
                {
                    'status_code': status.HTTP_200_OK,
                    'message': 'Customer items retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error('Unexpected error during listing Customers: %s', str(e))
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific `Customer` item by ID with custom response format.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            logger.info('Customer item retrieved successfully. ID: %d', instance.id)
            return Response(
                {
                    'status_code': status.HTTP_200_OK,
                    'message': 'Customer item retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except self.get_object().DoesNotExist:
            logger.warning('Customer item not found.')
            return Response(
                {
                    'status_code': status.HTTP_404_NOT_FOUND,
                    'message': 'Customer item not found.',
                }, status=status.HTTP_404_NOT_FOUND,
            )
        except PermissionDenied:
            logger.warning('Permission denied for retrieving Customer item.')
            return Response(
                {
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'Permission denied.',
                }, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            logger.error('Unexpected error during Customer retrieval: %s', str(e))
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        """
        Update a specific `Customer` item with custom response format.
        """
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)

                logger.info('Customer updated successfully. ID: %d', instance.id)
                return Response(
                    {
                        'status_code': status.HTTP_200_OK,
                        'message': 'Customer updated successfully.',
                        'data': serializer.data,
                    }, status=status.HTTP_200_OK,
                )
            else:
                logger.warning('Invalid data for Customer update: %s', serializer.errors)
                return Response(
                    {
                        'status_code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid data.',
                        'data': serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST,
                )
        except ValidationError as e:
            logger.error('Validation error during Customer update: %s', e.detail)
            return Response(
                {
                    'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'message': 'Validation error.',
                    'data': e.detail,
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error('Unexpected error during Customer update: %s', str(e))
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific `Customer` item with custom response format.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)

            logger.info('Customer deleted successfully.')
            return Response(
                {
                    'status_code': status.HTTP_204_NO_CONTENT,
                    'message': 'Customer deleted successfully.',
                }, status=status.HTTP_204_NO_CONTENT,
            )
        except PermissionDenied:
            logger.warning('Permission denied for deleting Customer item.')
            return Response(
                {
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'Permission denied.',
                }, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            logger.error('Unexpected error during Customer deletion: %s', str(e))
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
