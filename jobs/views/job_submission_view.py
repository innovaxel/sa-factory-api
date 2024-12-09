from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config

from common.auth import JWTAuthentication
from common.blob_storage import AzureBlobUploader
from jobs.models import JobTrackingEntry
from jobs.models.job_tracking_image import JobTrackingEntryImage
from jobs.serializers import JobEntrySubmissionSerializer


from decouple import config


class JobSubmissionView(APIView):

    permission_classes = [JWTAuthentication]

    queryset = JobTrackingEntry.objects.all()
    serializer_class = JobEntrySubmissionSerializer

    def post(self, request, *args, **kwargs):
        # Print the environment variables to check if they are loaded
        container_url = config("CONTAINER_URL")
        blob_storage_token = config("BLOB_STORAGE_TOKEN")
        container_name = config("CONTAINER_NAME")

        # Print them in the server logs for debugging
        print(f"Container URL: {container_url}")
        print(f"Blob Storage Token: {blob_storage_token}")
        print(f"Container Name: {container_name}")

        # Create a mutable copy of the request data
        data = request.data.copy()

        # Add the start time and HR ID to the copied data
        data["entry_start_time"] = timezone.now()
        user_hr_id = request.user.get("hr_id")
        data["entry_hr"] = user_hr_id

        entry_task_gid = data.get("entry_task_gid")

        existing_entry = JobTrackingEntry.objects.filter(
            entry_task_gid=entry_task_gid, entry_is_complete=True
        ).first()

        if existing_entry:
            return Response(
                {
                    "message": "Task is already complete",
                    "error": "This task has already been marked as complete.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Access the media files
        media_files = request.FILES.getlist("media")  # Use 'media' as the key
        print(f"Number of media files received: {len(media_files)}")

        # Initialize AzureBlobUploader for 'factory-app' container
        blob_uploader = AzureBlobUploader(
            container_url=container_url,
            token=blob_storage_token,
            container_name=container_name,
        )

        # Upload media files
        uploaded_urls = blob_uploader.upload_multiple_files(media_files)

        # Save the job tracking entry
        entry_serializer = self.serializer_class(data=data)
        entry_serializer.is_valid(raise_exception=True)
        job_tracking_entry = entry_serializer.save()

        # Save the uploaded media URLs into the database
        for file_url in uploaded_urls:
            JobTrackingEntryImage.objects.create(
                entry_id=job_tracking_entry,
                entry_image_url=file_url,
            )

        return Response(
            {"message": "Job Submission entered successfully"},
            status=status.HTTP_201_CREATED,
        )
