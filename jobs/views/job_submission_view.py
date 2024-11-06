from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from common.auth import JWTAuthentication

from jobs.models import JobTrackingEntry
from jobs.models.job_tracking_image import JobTrackingEntryImage
from jobs.serializers import JobEntrySubmissionSerializer


class JobSubmissionView(APIView):

    permission_classes = [JWTAuthentication]

    queryset = JobTrackingEntry.objects.all()
    serializer_class = JobEntrySubmissionSerializer

    def post(self, request, *args, **kwargs):
        request.data["entry_start_time"] = timezone.now()
        user_hr_id = request.user.get("hr_id")
        request.data["entry_hr"] = user_hr_id

        entry_task_gid = request.data.get("entry_task_gid")

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

        entry_serializer = self.serializer_class(data=request.data)
        entry_serializer.is_valid(raise_exception=True)
        job_tracking_entry = entry_serializer.save()

        images_data = request.data.get("images", [])
        for image_url in images_data:
            JobTrackingEntryImage.objects.create(
                entry_id=job_tracking_entry,
                entry_image_url=image_url,
            )

        return Response(
            {"message": "Job Submission entered successfully"},
            status=status.HTTP_201_CREATED,
        )
