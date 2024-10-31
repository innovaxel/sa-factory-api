# """
# ViewSet for managing `Job` instances.

# This module defines the `JobViewSet` class, which provides CRUD operations
# for `Job` instances.
# The `JobViewSet` class includes methods for listing, creating, retrieving,
# updating, and deleting
# `Job` instances, with custom response formats for each operation.

# - `create`: Handles the creation of new `Job` instances with a custom response format.
# - `list`: Lists all `Job` instances with a custom response format.
# - `retrieve`: Retrieves and returns a specific `Job` instance by ID with a custom
#                 response format.
# - `update`: Updates an existing `Job` instance with a custom response format.
# - `destroy`: Deletes a specific `Job` instance with a custom response format.
# """
# from __future__ import annotations

# import logging

# from datetime import timedelta
# from django.utils import timezone
# from rest_framework import status, viewsets, generics
# from rest_framework.views import APIView
# from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny, IsAuthenticated

# from common.device_validator import DeviceValidator
# from accounts.permission import IsAdminOrReadOnly
# from jobs.models import Job, JobLog, Timesheet

# from common.utility_functions import TimeCalculator
# from jobs.serializers import JobSerializer, ChipSerializer


# logger = logging.getLogger('jobs')


# class JobViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing Job instances.

#     Provides methods for creating, listing, retrieving, updating,
#     and deleting Job instances.
#     """
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer

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
#         Create a new `Job` instance with custom response format.

#         Validates the incoming data, creates a new Job instance,
#         and returns a success response.
#         """
#         serializer = self.get_serializer(data=request.data)
#         try:
#             if serializer.is_valid():
#                 serializer.save()
#                 headers = self.get_success_headers(serializer.data)

#                 logger.info('Job created successfully.')
#                 return Response(
#                     {
#                         'message': 'Job created successfully.',
#                         'data': serializer.data,
#                     }, status=status.HTTP_201_CREATED, headers=headers,
#                 )
#             else:
#                 logger.error('Invalid data.')
#                 return Response(
#                     {
#                         'message': 'Invalid data.',
#                         'errors': serializer.errors,
#                     }, status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except ValidationError as e:
#             logger.error('Validation error. %s', e.detail)
#             return Response(
#                 {
#                     'message': 'Validation error.',
#                     'data': e.detail,
#                 }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )
#         except Exception as e:
#             logger.error('An error occurred. %s', str(e))
#             return Response(
#                 {
#                     'message': str(e),
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#     def list(self, request, *args, **kwargs):
#         """
#         List all `Job` instances with custom response format.

#         Retrieves all Job instances, serializes them, and returns a success response.
#         """
#         device_id = request.data.get('device_id')

#         validator = DeviceValidator(device_id)
#         response = validator.validate()
#         if response:
#             return response

#         try:
#             queryset = self.filter_queryset(self.get_queryset())
#             serializer = self.get_serializer(
#                 queryset, many=True,
#             )
#             logger.info('Job items retrieved successfully.')
#             return Response(
#                 {
#                     'message': 'Job items retrieved successfully.',
#                     'data': serializer.data,
#                 }, status=status.HTTP_200_OK,
#             )
#         except Exception as e:
#             logger.error('An error occurred. %s', str(e))
#             return Response(
#                 {
#                     'message': str(e),
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#     def retrieve(self, request, *args, **kwargs):
#         """
#         Retrieve a specific `Job` instance by ID with custom response format.

#         Retrieves a single Job instance, serializes it, and returns a success response.
#         """
#         device_id = request.data.get('device_id')

#         validator = DeviceValidator(device_id)
#         response = validator.validate()
#         if response:
#             return response

#         try:
#             instance = self.get_object()
#             serializer = self.get_serializer(instance)

#             logger.info('Job item retrieved successfully.')
#             return Response(
#                 {
#                     'message': 'Job item retrieved successfully.',
#                     'data': serializer.data,
#                 }, status=status.HTTP_200_OK,
#             )
#         except self.get_object().DoesNotExist:
#             logger.error('Job oes not exist.')
#             return Response(
#                 {
#                     'message': 'Job item not found.',
#                 }, status=status.HTTP_404_NOT_FOUND,
#             )
#         except PermissionDenied:
#             logger.error('Permission denied.')
#             return Response(
#                 {
#                     'message': 'Permission denied.',
#                 }, status=status.HTTP_403_FORBIDDEN,
#             )
#         except Exception as e:
#             logger.error('An error occurred. %s', str(e))
#             return Response(
#                 {
#                     'message': str(e),
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#     def update(self, request, *args, **kwargs):
#         """
#         Update a specific `Job` instance with custom response format.

#         Validates and updates an existing Job instance, then returns a success response.
#         """
#         partial = kwargs.pop('partial', False)
#         try:
#             instance = self.get_object()
#             serializer = self.get_serializer(instance, data=request.data, partial=partial)
#             if serializer.is_valid():

#                 logger.info('Job updated successfully.')
#                 self.perform_update(serializer)
#                 return Response(
#                     {
#                         'message': 'Job updated successfully.',
#                         'data': serializer.data,
#                     }, status=status.HTTP_200_OK,
#                 )
#             else:
#                 logger.error('Invalid data.')
#                 return Response(
#                     {
#                         'message': 'Invalid data.',
#                         'errors': serializer.errors,
#                     }, status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except ValidationError as e:
#             logger.error('Validation error. %s', e.detail)
#             return Response(
#                 {
#                     'message': 'Validation error.',
#                     'data': e.detail,
#                 }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )
#         except Exception as e:
#             logger.error('An error occurred. %s', str(e))
#             return Response(
#                 {
#                     'message': str(e),
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#     def destroy(self, request, *args, **kwargs):
#         """
#         Delete a specific `Job` instance with custom response format.

#         Deletes an existing Job instance and returns a success response.
#         """
#         try:
#             instance = self.get_object()
#             self.perform_destroy(instance)

#             logger.info('Job deleted successfully.')
#             return Response(
#                 {
#                     'message': 'Job deleted successfully.',
#                 }, status=status.HTTP_204_NO_CONTENT,
#             )
#         except PermissionDenied:
#             logger.error('Permission denied.')
#             return Response(
#                 {
#                     'message': 'Permission denied.',
#                 }, status=status.HTTP_403_FORBIDDEN,
#             )
#         except Exception as e:
#             logger.error('An error occurred. %s', str(e))
#             return Response(
#                 {
#                     'message': str(e),
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


# class JobByWorkListView(generics.ListAPIView):
#     """
#     View to list all jobs in a specific worklist.

#     Accepts a worklist ID as a URL parameter and returns all associated jobs.
#     """
#     serializer_class = JobSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """
#         Override get_queryset to filter jobs by worklist ID from the URL.
#         """
#         worklist_id = self.kwargs.get('worklist_id')
#         return Job.objects.filter(worklistid=worklist_id, status='in_progress')

#     def list(self, request, *args, **kwargs):
#         """
#         Override list to provide a custom response.
#         """
#         device_id = request.data.get('device_id')

#         validator = DeviceValidator(device_id)
#         response = validator.validate()
#         if response:
#             return response

#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({
#             'message': 'Jobs in the specified worklist',
#             'data': {
#                 'worklist_id': self.kwargs.get('worklist_id'),
#                 'jobs': serializer.data,
#             },
#         })


# class JobLogView(APIView):
#     """
#     API view to retrieve users who have worked on a specific job.
#     """

#     def get(self, request, job_id):
#         """
#         Retrieves users who have worked on the job specified by job_id.
#         """
#         device_id = request.data.get('device_id')

#         validator = DeviceValidator(device_id)
#         response = validator.validate()
#         if response:
#             return response

#         try:
#             job_logs = JobLog.objects.filter(job_id=job_id)
#             if not job_logs.exists():
#                 logger.error('Job not found.')
#                 raise NotFound('Job not found or no logs available for this job.')

#             users = {log.user for log in job_logs}
#             user_data = []

#             login_user = request.user

#             total_time_current_user = TimeCalculator.calculate_current_user_time(
#                 login_user, job_id,
#             )
#             total_time_current_user_str = TimeCalculator.format_total_time(
#                 total_time_current_user,
#             )

#             for user in users:
#                 if user.id == login_user.id:
#                     continue

#                 total_time_other_user = TimeCalculator.calculate_other_user_time(
#                     user, job_id,
#                 )
#                 total_time_other_user_str = TimeCalculator.format_total_time(
#                     total_time_other_user,
#                 )

#                 user_data.append({
#                     'id': user.id,
#                     'full_name': user.full_name,
#                     'role': user.role,
#                     'total_time_spent': total_time_other_user_str,
#                 })

#             logger.info(
#                 'Users who have worked on the job retrieved successfully. count=%s',
#                 len(user_data),
#             )
#             return Response({
#                 'message': 'Users who have worked on the job',
#                 'data': {
#                     'job_id': job_id,
#                     'current_user_total_time': total_time_current_user_str,
#                     'users': user_data,
#                 },
#             })

#         except NotFound:
#             logger.error('Job not found.')
#             return Response(
#                 {
#                     'message': 'Job not found or no logs available for this job',
#                     'data': {},
#                 }, status=status.HTTP_404_NOT_FOUND,
#             )

#         except PermissionDenied:
#             logger.error('Permission denied.')
#             return Response(
#                 {
#                     'message': 'You do not have permission to access this resource',
#                     'data': {},
#                 }, status=status.HTTP_403_FORBIDDEN,
#             )

#         except Exception as e:
#             logger.error('Internal server error. %s', str(e))
#             return Response(
#                 {
#                     'message': f"An unexpected error occurred: {str(e)}",
#                     'data': {},
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


# class UserJobsView(APIView):
#     """
#     API view to retrieve unique jobs that a specific user
#     has worked on in the last 7 days.
#     """

#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """
#         Retrieves unique jobs that the user specified by user_id has
#         worked on in the last 7 days.

#         Args:
#             request: The HTTP request object.

#         Returns:
#             Response: A Response object containing the status
#             code, message, and job data.
#         """
#         user = request.user
#         device_id = request.data.get('device_id')

#         validator = DeviceValidator(device_id)
#         response = validator.validate()
#         if response:
#             return response

#         try:
#             if not user:
#                 logger.error('User not found.')
#                 return Response(
#                     {
#                         'message': 'User not found.',
#                     }, status=status.HTTP_404_NOT_FOUND,
#                 )

#             seven_days_ago = timezone.now() - timedelta(days=7)

#             job_logs = Timesheet.objects.filter(
#                 user_id=user.id,
#                 timestamp__gte=seven_days_ago,
#             )
#             if not job_logs.exists():
#                 logger.error('No jobs available for this user in the last 7 days.')
#                 return Response(
#                     {
#                         'message': 'No jobs available in the last 7 days.',
#                     }, status=status.HTTP_404_NOT_FOUND,
#                 )

#             unique_job_ids = {log.job_id.id for log in job_logs}

#             jobs = Job.objects.filter(id__in=unique_job_ids)
#             serializer = JobSerializer(jobs, many=True, context={'request': request})

#             logger.info(
#                 'Jobs that user worked on retrieved successfully. count=%s',
#                 len(jobs),
#             )
#             return Response({
#                 'message': 'Jobs user has worked on in the last 7 days',
#                 'data': {
#                     'user_id': user.id,
#                     'jobs': serializer.data,
#                 },
#             })

#         except PermissionDenied as e:
#             logger.error('Permission denied. %s', str(e))
#             return Response(
#                 {
#                     'message': str(e),
#                 }, status=status.HTTP_403_FORBIDDEN,
#             )

#         except Exception as e:
#             logger.error('Internal server error. %s', str(e))
#             return Response(
#                 {
#                     'message': f"An unexpected error occurred: {str(e)}",
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


# class JobDetailView(APIView):
#     """
#     API view to retrieve users who have worked on a specific
#     job and the unique jobs a user has worked on in the last 7 days.
#     """

#     permission_classes = [IsAuthenticated]

#     def get(self, request, job_id):
#         """
#         Retrieves users who have worked on the job specified by job_id
#         and the unique jobs that the requesting user has worked on in the last 7 days.
#         """
#         device_id = request.data.get('device_id')

#         validator = DeviceValidator(device_id)
#         response = validator.validate()
#         if response:
#             return response

#         try:
#             job_logs = JobLog.objects.filter(job_id=job_id)
#             if not job_logs.exists():
#                 logger.error('Job not found.')
#                 return Response(
#                     {
#                         'message': 'Job not found or no logs available for this job',
#                         'data': {},
#                     }, status=status.HTTP_404_NOT_FOUND,
#                 )

#             users = {log.user for log in job_logs}
#             user_data = []
#             login_user = request.user

#             total_time_current_user = TimeCalculator.calculate_current_user_time(
#                 login_user, job_id,
#             )
#             total_time_current_user_str = TimeCalculator.format_total_time(
#                 total_time_current_user,
#             )

#             for user in users:
#                 if user.id == login_user.id:
#                     continue

#                 total_time_other_user = TimeCalculator.calculate_other_user_time(
#                     user, job_id,
#                 )
#                 total_time_other_user_str = TimeCalculator.format_total_time(
#                     total_time_other_user,
#                 )

#                 chip = TimeCalculator.get_chip_based_on_time_spent(
#                     total_time_other_user_str,
#                 )
#                 chip_serializer = ChipSerializer(chip)

#                 user_data.append({
#                     'id': user.id,
#                     'full_name': user.full_name,
#                     'role': user.role,
#                     'total_time_spent': total_time_other_user_str,
#                     'chip': chip_serializer.data,
#                 })

#             seven_days_ago = timezone.now() - timedelta(days=7)
#             job_logs_last_7_days = Timesheet.objects.filter(
#                 user_id=login_user.id,
#                 timestamp__gte=seven_days_ago,
#             )

#             unique_job_ids = {log.job_id.id for log in job_logs_last_7_days}
#             jobs = Job.objects.filter(id__in=unique_job_ids)

#             if not jobs.exists():
#                 logger.warning('No jobs available in the last 7 days for user.')
#                 jobs_data = {
#                     'message': 'No jobs available in the last 7 days.',
#                     'jobs': [],
#                 }
#             else:
#                 job_serializer = JobSerializer(
#                     jobs, many=True, context={'request': request},
#                 )
#                 jobs_data = {
#                     'jobs': job_serializer.data,
#                 }

#             logger.info(
#                 'Users who have worked on the job retrieved successfully. count=%s',
#                 len(user_data),
#             )

#             return Response({
#                 'message': 'Users who have worked on the job',
#                 'data': {
#                     'job_id': job_id,
#                     'time_spent': total_time_current_user_str,
#                     'users': user_data,
#                     **jobs_data,
#                 },
#             })

#         except PermissionDenied:
#             logger.error('Permission denied.')
#             return Response(
#                 {
#                     'message': 'You do not have permission to access this resource',
#                     'data': {},
#                 }, status=status.HTTP_403_FORBIDDEN,
#             )

#         except Exception as e:
#             logger.error('Internal server error. %s', str(e))
#             return Response(
#                 {
#                     'message': f"An unexpected error occurred: {str(e)}",
#                     'data': {},
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from jobs.models import AsanaTask
from jobs.serializers import AsanaTaskSerializer


class AsanaTaskListView(APIView):
    def get(self, request):
        tasks = AsanaTask.objects.all()
        serializer = AsanaTaskSerializer(tasks, many=True)
        return Response(
            {
                "message": "Success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class AsanaTaskByWorklistView(APIView):
    def get(self, request, worklist_id):
        tasks = AsanaTask.objects.all()
        serializer = AsanaTaskSerializer(tasks, many=True)
        return Response(
            {
                "message": "Success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
