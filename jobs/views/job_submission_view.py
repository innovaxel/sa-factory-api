"""
ViewSet for managing `JobSubmission` entries.

This module defines the `JobSubmissionViewSet` class, which provides operations
for creating and listing job submissions. The `JobSubmissionViewSet`
class includes methods
for creating new job submissions, listing all submissions, and retrieving
specific submissions.
It also handles media file uploads associated with job submissions.

- `perform_create`: Custom method to assign the logged-in user to the `JobSubmission`
                    and handle media uploads.
- `create`: Handles the creation of new `JobSubmission` entries with validation and
            appropriate responses based on the action. Logs the creation of
            job submissions and associates them with the authenticated user.
- `list`: Retrieves a list of all `JobSubmission` entries along with
            their related media.
- `retrieve`: Retrieves a specific `JobSubmission` entry along with its
                related media by ID.
"""
from __future__ import annotations

import logging

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from common.device_validator import DeviceValidator
from jobs.models import JobSubmission, Media, Job, JobLog
from jobs.serializers import JobSubmissionSerializer, MediaSerializer

logger = logging.getLogger('jobs')


class JobSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for creating and listing JobSubmissions.
    The `user` field is automatically assigned to the currently authenticated user.
    Also handles uploading media files related to the JobSubmission.
    """
    serializer_class = JobSubmissionSerializer
    queryset = JobSubmission.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom method to assign the logged-in user to the JobSubmission
        and handle media uploads.
        """
        job_submission = serializer.save(user=self.request.user)

        try:
            job = Job.objects.get(id=serializer.validated_data['job_id'])
            JobLog.objects.create(user=self.request.user, job=job, status='completed')

            media_files = self.request.FILES.getlist('media')
            for media in media_files:
                Media.objects.create(resource_id=job_submission.id, image=media)
        except Job.DoesNotExist:
            logger.error(
                'Job with ID %s does not exist when creating JobSubmission.',
                serializer.validated_data['job_id']
            )
            raise serializers.ValidationError('Job with this ID does not exist.')

    def create(self, request, *args, **kwargs):
        """
        Create a new `JobSubmission` with the logged-in user as the submitter.
        Also handles media files if provided.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        request_data = request.data.copy()
        serializer = self.get_serializer(data=request_data)

        try:
            if serializer.is_valid():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)

                logger.info('JobSubmission created successfully.')
                return Response(
                    {
                        'message': 'JobSubmission created successfully.',
                    }, status=status.HTTP_201_CREATED, headers=headers,
                )
            else:
                logger.error('Invalid data for JobSubmission.')
                return Response(
                    {
                        'message': 'Invalid data.',
                        'errors': serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST,
                )
        except ValidationError as e:
            logger.error('Validation error in JobSubmission: %s', e.detail)
            return Response(
                {
                    'message': 'Validation error.',
                    'errors': e.detail,
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error('Error creating JobSubmission: %s', str(e))
            return Response(
                {
                    'message': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all JobSubmissions along with their related media.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        job_submissions = JobSubmission.objects.all()
        data = []
        for job_submission in job_submissions:
            job_submission_data = JobSubmissionSerializer(job_submission).data

            media_files = Media.objects.filter(resource_id=job_submission.id)
            media_data = MediaSerializer(media_files, many=True).data

            job_submission_data['media'] = media_data
            data.append(job_submission_data)

        return Response(
            {
                'message': 'List of all JobSubmissions with media files.',
                'data': data,
            }, status=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific JobSubmission along with its related media by ID.
        """
        device_id = request.data.get('device_id')

        validator = DeviceValidator(device_id)
        response = validator.validate()
        if response:
            return response

        job_submission = self.get_object()

        job_submission_data = JobSubmissionSerializer(job_submission).data

        media_files = Media.objects.filter(resource_id=job_submission.id)
        media_data = MediaSerializer(media_files, many=True).data

        job_submission_data['media'] = media_data

        return Response(
            {
                'message': 'JobSubmission with media files retrieved successfully.',
                'data': job_submission_data,
            }, status=status.HTTP_200_OK,
        )
