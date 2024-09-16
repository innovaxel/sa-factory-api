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

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from jobs.models import WorkList
from jobs.serializers import WorkListSerializer

class WorkListViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing `WorkList` items.

    Provides CRUD operations for `WorkList` instances, including list,
    create, retrieve, update, and delete operations.
    """
    queryset = WorkList.objects.all()
    serializer_class = WorkListSerializer

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
                return Response({
                    'status_code': status.HTTP_201_CREATED,
                    'message': 'WorkList item created successfully.',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response({
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid data.',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({
                'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'Validation error.',
                'data': e.detail
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            return Response({
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                return Response({
                    'status_code': status.HTTP_200_OK,
                    'message': 'WorkList item updated successfully.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid data.',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({
                'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'Validation error.',
                'data': e.detail
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            return Response({
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes an existing `WorkList` item.

        Returns success or error responses based on the result of the
        deletion operation.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status_code': status.HTTP_204_NO_CONTENT,
            'message': 'WorkList item deleted successfully.',
        }, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        List all `WorkList` items with a custom response format.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'status_code': status.HTTP_200_OK,
                'message': 'WorkList items retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific `WorkList` item by ID with a custom response format.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'status_code': status.HTTP_200_OK,
                'message': 'WorkList item retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
