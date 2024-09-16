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

from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from jobs.models import JobAddress
from jobs.serializers import JobAddressSerializer


class JobAddressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Job Address. Allows
    listing, creating, and modifying, and deleting Job Address.
    Job Address with different permissions for simple users and admins.
    """

    queryset = JobAddress.objects.all()
    serializer_class = JobAddressSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new `JobAddress` item with custom response format.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(
                    {
                        'status_code': status.HTTP_201_CREATED,
                        'message': 'JobAddress created successfully.',
                        'data': serializer.data,
                    }, status=status.HTTP_201_CREATED, headers=headers,
                )
            else:
                return Response(
                    {
                        'status_code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid data.',
                        'data': serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST,
                )
        except ValidationError as e:
            return Response(
                {
                    'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'message': 'Validation error.',
                    'data': e.detail,
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e),
                    'data': None,
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request, *args, **kwargs):
        """
        List all `JobAddress` items with custom response format.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    'status_code': status.HTTP_200_OK,
                    'message': 'JobAddress items retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e),
                    'data': None,
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific `JobAddress` item by ID with custom response format.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {
                    'status_code': status.HTTP_200_OK,
                    'message': 'JobAddress item retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except self.get_object().DoesNotExist:
            return Response(
                {
                    'status_code': status.HTTP_404_NOT_FOUND,
                    'message': 'JobAddress item not found.',
                    'data': None,
                }, status=status.HTTP_404_NOT_FOUND,
            )
        except PermissionDenied:
            return Response(
                {
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'Permission denied.',
                    'data': None,
                }, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
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
                return Response(
                    {
                        'status_code': status.HTTP_200_OK,
                        'message': 'JobAddress updated successfully.',
                        'data': serializer.data,
                    }, status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        'status_code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid data.',
                        'data': serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST,
                )
        except ValidationError as e:
            return Response(
                {
                    'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'message': 'Validation error.',
                    'data': e.detail,
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            return Response(
                {
                    'status_code': status.HTTP_204_NO_CONTENT,
                    'message': 'JobAddress deleted successfully.',
                    'data': None,
                }, status=status.HTTP_204_NO_CONTENT,
            )
        except PermissionDenied:
            return Response(
                {
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'Permission denied.',
                    'data': None,
                }, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e),
                    'data': None,
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
