"""
ViewSet for managing `Location` instances.

This module defines the `LocationViewSet` class, which provides 
CRUD operations for `Location` instances.
The `LocationViewSet` class includes methods for listing, creating, 
retrieving, updating, and deleting 
`Location` instances, with custom response formats for each operation.

- `create`: Creates a new `Location` instance with a custom 
                response format. Handles validation and errors.
- `update`: Updates an existing `Location` instance with a custom 
                response format. Handles validation and errors.
- `destroy`: Deletes a specific `Location` instance with a 
                custom response format. Handles errors.
- `list`: Lists all `Location` instances with a custom response format. 
            Includes associated worklists.
- `retrieve`: Retrieves and returns a specific `Location` 
                instance by ID with a custom response format. Includes associated worklists.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError


from jobs.models import Location
from jobs.serializers import LocationSerializer



class LocationViewSet(ModelViewSet):
    """
    ViewSet for managing locations. Allows 
    listing, creating, and modifying, and deleting locations.
    locations with different permissions for simple users and admins.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new location instance. Handles validation and
        error cases for better response formatting.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response({
                    'status_code': status.HTTP_201_CREATED,
                    'message': 'Location created successfully.',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED, headers=headers)
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
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        Update a location instance. Handles validation and error cases.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response({
                    'status_code': status.HTTP_200_OK,
                    'message': 'Location updated successfully.',
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
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """
            Delete a location instance. Handles error cases.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'status_code': status.HTTP_204_NO_CONTENT,
                'message': 'Location deleted successfully.',
                'data': None
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        """
        Customize the response format for listing locations.
        Now includes associated worklists.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status_code': status.HTTP_200_OK,
            'message': 'Locations retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Customize the response format for retrieving a single location.
        Now includes associated worklists.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status_code': status.HTTP_200_OK,
            'message': 'Location retrieved successfully.',
            'data': [serializer.data]
        }, status=status.HTTP_200_OK)
