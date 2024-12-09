from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.auth import JWTAuthentication
from common.blob_storage import AzureBlobUploader
from jobs.models import JobTrackingEntry
from jobs.models.job_tracking_image import JobTrackingEntryImage
from jobs.serializers import JobEntrySubmissionSerializer


class JobSubmissionView(APIView):
    permission_classes = [JWTAuthentication]

    queryset = JobTrackingEntry.objects.all()
    serializer_class = JobEntrySubmissionSerializer

    def post(self, request, *args, **kwargs):
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
            container_url="https://cs11003bffdac6d8d99.blob.core.windows.net/factory-app",
            token="?sv=2023-01-03&st=2024-11-28T21%3A15%3A41Z&se=2025-11-27T21%3A15%3A00Z&sr=c&sp=racwl&sig=uJHBoudMakgIg9wRyTt0S6CnG%2FK1NYcCHgPfMG2NrQk%3D",
            container_name="factory-app",  # Pass the container name
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
