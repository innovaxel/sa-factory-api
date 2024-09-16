"""
ViewSet for managing `Job` instances.

This module defines the `JobViewSet` class, which provides CRUD operations
for `Job` instances.
The `JobViewSet` class includes methods for listing, creating, retrieving,
updating, and deleting
`Job` instances, with custom response formats for each operation.

- `create`: Handles the creation of new `Job` instances with a custom response format.
- `list`: Lists all `Job` instances with a custom response format.
- `retrieve`: Retrieves and returns a specific `Job` instance by ID with a custom
                response format.
- `update`: Updates an existing `Job` instance with a custom response format.
- `destroy`: Deletes a specific `Job` instance with a custom response format.
"""
from __future__ import annotations

from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from jobs.models import Job
from jobs.serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Job instances.

    Provides methods for creating, listing, retrieving, updating,
    and deleting Job instances.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new `Job` instance with custom response format.

        Validates the incoming data, creates a new Job instance,
        and returns a success response.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                return Response(
                    {
                        'status_code': status.HTTP_201_CREATED,
                        'message': 'Job created successfully.',
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
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request, *args, **kwargs):
        """
        List all `Job` instances with custom response format.

        Retrieves all Job instances, serializes them, and returns a success response.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    'status_code': status.HTTP_200_OK,
                    'message': 'Job items retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific `Job` instance by ID with custom response format.

        Retrieves a single Job instance, serializes it, and returns a success response.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {
                    'status_code': status.HTTP_200_OK,
                    'message': 'Job item retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except self.get_object().DoesNotExist:
            return Response(
                {
                    'status_code': status.HTTP_404_NOT_FOUND,
                    'message': 'Job item not found.',
                }, status=status.HTTP_404_NOT_FOUND,
            )
        except PermissionDenied:
            return Response(
                {
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'Permission denied.',
                }, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        """
        Update a specific `Job` instance with custom response format.

        Validates and updates an existing Job instance, then returns a success response.
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
                        'message': 'Job updated successfully.',
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
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific `Job` instance with custom response format.

        Deletes an existing Job instance and returns a success response.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {
                    'status_code': status.HTTP_204_NO_CONTENT,
                    'message': 'Job deleted successfully.',
                }, status=status.HTTP_204_NO_CONTENT,
            )
        except PermissionDenied:
            return Response(
                {
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'Permission denied.',
                }, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                {
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
