# """
# ViewSet for the `ErrorCategory` model.

# This module defines the `ErrorCategoryViewSet` class, which provides CRUD operations for
# `ErrorCategory` instances. The `ErrorCategoryViewSet` class includes methods for listing,
# creating, retrieving, updating, and deleting `ErrorCategory`
# instances, with custom response
# formats for each operation.

# - `create`: Handles creation of new `ErrorCategory` instances
#             with a custom response format.
# - `update`: Updates an existing `ErrorCategory` instance with a custom response format.
# - `destroy`: Deletes a specific `ErrorCategory` instance with a custom response format.
# - `list`: Retrieves and lists all `ErrorCategory` instances with a custom response format.
# """
# from __future__ import annotations

# import logging

# from rest_framework import status, viewsets
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny

# from common.device_validator import DeviceValidator
# from accounts.permission import IsAdminOrReadOnly

# from jobs.models import ErrorCategory
# from jobs.serializers import ErrorCategorySerializer

# logger = logging.getLogger('jobs')


# class ErrorCategoryViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for the ErrorCategory model.

#     Provides `list`, `create`, `retrieve`, `update`, and `delete` actions.
#     """
#     queryset = ErrorCategory.objects.all()
#     serializer_class = ErrorCategorySerializer

#     def get_permissions(self):
#         """
#         Return the permission classes based on the action.
#         """
#         if self.action in ['list', 'retrieve']:
#             return [AllowAny()]
#         if self.action in ['create', 'update', 'destroy']:
#             return [IsAdminOrReadOnly()]
#         return super().get_permissions()

#     def create(self, request, *args, **kwargs):
#         """
#         Create a new ErrorCategory with a custom response format.
#         """
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)

#             logger.info('ErrorCategory created successfully.')
#             return Response(
#                 {
#                     'message': 'ErrorCategory created successfully.',
#                     'data': serializer.data,
#                 }, status=status.HTTP_201_CREATED, headers=headers,
#             )
#         logger.error('Invalid data.')
#         return Response(
#             {
#                 'message': 'Invalid data.',
#                 'errors': serializer.errors,
#             }, status=status.HTTP_400_BAD_REQUEST,
#         )

#     def update(self, request, *args, **kwargs):
#         """
#         Update an existing ErrorCategory with a custom response format.
#         """
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         if serializer.is_valid():
#             self.perform_update(serializer)

#             logger.info('ErrorCategory updated successfully.')
#             return Response(
#                 {
#                     'message': 'ErrorCategory updated successfully.',
#                     'data': serializer.data,
#                 }, status=status.HTTP_200_OK,
#             )

#         logger.error('Invalid data.')
#         return Response(
#             {
#                 'message': 'Invalid data.',
#                 'errors': serializer.errors,
#             }, status=status.HTTP_400_BAD_REQUEST,
#         )

#     def destroy(self, request, *args, **kwargs):
#         """
#         Delete an ErrorCategory with a custom response format.
#         """
#         instance = self.get_object()
#         self.perform_destroy(instance)

#         logger.info('ErrorCategory deleted successfully.')
#         return Response(
#             {
#                 'message': 'ErrorCategory deleted successfully.',
#             }, status=status.HTTP_204_NO_CONTENT,
#         )

#     def list(self, request, *args, **kwargs):
#         """
#         List all ErrorCategory items with a custom response format.
#         """
#         device_id = request.data.get('device_id')

#         validator = DeviceValidator(device_id)
#         response = validator.validate()
#         if response:
#             return response

#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)

#         logger.info('ErrorCategory items retrieved successfully.')
#         return Response(
#             {
#                 'message': 'ErrorCategory items retrieved successfully.',
#                 'data': serializer.data,
#             }, status=status.HTTP_200_OK,
#         )
