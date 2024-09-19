"""
ViewSet for the `Chip` model.

This module defines the `ChipViewSet` class, which provides CRUD operations for
`Chip` instances. The `ChipViewSet` class includes methods for creating, listing,
retrieving, updating, and deleting `Chip` instances, with custom response formats
for each operation.

- `create`: Handles creation of new `Chip` instances.
- `list`: Retrieves and lists all `Chip` instances.
- `retrieve`: Retrieves a single `Chip` instance by its ID.
- `update`: Updates an existing `Chip` instance.
- `destroy`: Deletes a specific `Chip` instance.
"""
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny

from accounts.permission import IsAdminOrReadOnly
from common.device_validator import DeviceValidator

from jobs.models import Chip
from jobs.serializers import ChipSerializer

logger = logging.getLogger('jobs')


class ChipViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Chip instances.

    Provides methods for creating, listing, retrieving, updating,
    and deleting Chip instances.
    """
    queryset = Chip.objects.all()
    serializer_class = ChipSerializer

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
        Create a new `Chip` instance with custom response format.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                logger.info('Chip created successfully.')
                return Response(
                    {
                        'message': 'Chip created successfully.',
                        'data': serializer.data,
                        'error': [],
                    }, status=status.HTTP_201_CREATED, headers=headers,
                )
            else:
                logger.warning('Invalid data for Chip creation: %s', serializer.errors)
                return Response(
                    {
                        'message': 'Invalid data.',
                        'data': [],

                    }, status=status.HTTP_400_BAD_REQUEST,
                )
        except ValidationError as e:
            logger.error('Validation error during Chip creation: %s', e.detail)
            return Response(
                {
                    'message': 'Validation error.',
                    'data': e.detail,
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error('Unexpected error during Chip creation: %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request, *args, **kwargs):
        """
        List all `Chip` instances with custom response format.
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
                'Chip items retrieved successfully. Count:'
                ' %d', len(serializer.data),
            )
            return Response(
                {
                    'message': 'Chip items retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error('Unexpected error during listing Chips: %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific `Chip` instance by ID with custom response format.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            logger.info('Chip item retrieved successfully. ID: %d', instance.id)
            return Response(
                {
                    'message': 'Chip item retrieved successfully.',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK,
            )
        except self.get_object().DoesNotExist:
            logger.warning('Chip item not found. ID: %s', kwargs['pk'])
            return Response(
                {
                    'message': 'Chip item not found.',
                }, status=status.HTTP_404_NOT_FOUND,
            )
        except PermissionDenied:
            logger.warning(
                'Permission denied for retrieving Chip item. ID: %s', kwargs['pk'],
            )
            return Response(
                {
                    'message': 'Permission denied.',
                }, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            logger.error('Unexpected error during Chip retrieval: %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        """
        Update a specific `Chip` instance with custom response format.
        """
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)
                logger.info('Chip updated successfully. ID: %d', instance.id)
                return Response(
                    {
                        'message': 'Chip updated successfully.',
                        'data': serializer.data,
                    }, status=status.HTTP_200_OK,
                )
            else:
                logger.warning(f'Invalid data for Chip update: {serializer.errors}')
                return Response(
                    {
                        'message': 'Invalid data.',
                        'errors': serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST,
                )
        except ValidationError as e:
            logger.error(f'Validation error during Chip update: {e.detail}')
            return Response(
                {
                    'message': 'Validation error.',
                    'data': e.detail,
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error(f'Unexpected error during Chip update: {str(e)}')
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific `Chip` instance with custom response format.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            logger.info('Chip deleted successfully.')
            return Response(
                {
                    'message': 'Chip deleted successfully.',
                }, status=status.HTTP_204_NO_CONTENT,
            )
        except PermissionDenied:
            logger.warning(
                'Permission denied for deleting Chip item. ID: %s', kwargs['pk'],
            )
            return Response(
                {
                    'message': 'Permission denied.',
                }, status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            logger.error('Unexpected error during Chip deletion: %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
