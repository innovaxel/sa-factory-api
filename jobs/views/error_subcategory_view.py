"""
ViewSet for the `ErrorSubCategory` model.

This module defines the `ErrorSubCategoryViewSet` class, which provides CRUD operations for
`ErrorSubCategory` instances. The `ErrorSubCategoryViewSet` class includes methods for listing,
creating, retrieving, updating, and deleting `ErrorSubCategory` instances, with custom response
formats for each operation.

- `create`: Handles creation of new `ErrorSubCategory` instances with a custom response format.
- `update`: Updates an existing `ErrorSubCategory` instance with a custom response format.
- `destroy`: Deletes a specific `ErrorSubCategory` instance with a custom response format.
- `list`: Retrieves and lists all `ErrorSubCategory` instances with a custom response format.
- `retrieve`: Retrieves and returns a specific `ErrorSubCategory` 
                instance by ID with a custom response format.
"""


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError

from jobs.models import ErrorSubCategory
from jobs.serializers import ErrorSubCategorySerializer

class ErrorSubCategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ErrorSubCategory instances.

    Provides methods for creating, listing, retrieving, updating, and deleting ErrorSubCategory instances.
    """
    queryset = ErrorSubCategory.objects.all()
    serializer_class = ErrorSubCategorySerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new `ErrorSubCategory` instance with custom response format.

        Validates the incoming data, creates a new ErrorSubCategory instance, and returns a success response.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                return Response({
                    'status_code': status.HTTP_201_CREATED,
                    'message': 'ErrorSubCategory created successfully.',
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

    def list(self, request, *args, **kwargs):
        """
        List all `ErrorSubCategory` instances with custom response format.

        Retrieves all ErrorSubCategory instances, serializes them, and returns a success response.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'status_code': status.HTTP_200_OK,
                'message': 'ErrorSubCategory items retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific `ErrorSubCategory` instance by ID with custom response format.

        Retrieves a single ErrorSubCategory instance, serializes it, and returns a success response.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'status_code': status.HTTP_200_OK,
                'message': 'ErrorSubCategory item retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except self.get_object().DoesNotExist:
            return Response({
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'ErrorSubCategory item not found.',
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'Permission denied.',
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        Update a specific `ErrorSubCategory` instance with custom response format.

        Validates and updates an existing ErrorSubCategory instance, then returns a success response.
        """
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response({
                    'status_code': status.HTTP_200_OK,
                    'message': 'ErrorSubCategory updated successfully.',
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
        Delete a specific `ErrorSubCategory` instance with custom response format.

        Deletes an existing ErrorSubCategory instance and returns a success response.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'status_code': status.HTTP_204_NO_CONTENT,
                'message': 'ErrorSubCategory deleted successfully.',
            }, status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied:
            return Response({
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'Permission denied.',
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
