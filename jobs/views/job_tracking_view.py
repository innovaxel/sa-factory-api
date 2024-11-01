from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models.human_resource import HumanResource
from jobs.models import JobTrackingEntry
from jobs.serializers import JobTrackingEntrySerializer
from django.utils import timezone
from common.auth import JWTAuthentication

from accounts.serializers.human_resource_serializer import (
    HumanResourceSerializer,
)


class JobTrackingView(APIView):
    permission_classes = [JWTAuthentication]

    def calculate_total_time_for_last_job(self, hr_id, task_gid):
        last_entry = (
            JobTrackingEntry.objects.filter(
                entry_task_gid=task_gid,
                entry_hr=hr_id,
                entry_end_time__isnull=False,
            )
            .order_by("-entry_end_time")
            .first()
        )

        if last_entry:
            total_duration = (
                last_entry.entry_end_time - last_entry.entry_start_time
            )
            return total_duration

        return timedelta()

    def get_user_jobs_last_7_days(self, hr_id):
        # Calculate the date 7 days ago from today
        last_7_days = timezone.now().date() - timedelta(days=7)

        # Filter JobTrackingEntry records for the logged-in user in the last 7 days
        recent_entries = JobTrackingEntry.objects.filter(
            entry_hr_id=hr_id, entry_date__gte=last_7_days
        )

        jobs = []
        task_time_map = {}

        for entry in recent_entries:
            if entry.entry_end_time and entry.entry_start_time:
                total_duration = entry.entry_end_time - entry.entry_start_time
                total_time_str = str(
                    total_duration
                )  # Convert duration to string format

                task_gid = entry.entry_task_gid.task_gid
                task_name = entry.entry_task_gid.task_name
                stair_category = entry.entry_task_gid.stair_category

                # Update the map with total time spent per task_gid
                if task_gid not in task_time_map:
                    task_time_map[task_gid] = {
                        "id": task_gid,
                        "name": task_name,
                        "stair_category": stair_category,
                        "total_time": total_time_str,
                    }

        jobs = list(task_time_map.values())
        return jobs

    def post(self, request):
        action = request.data.get("action")
        user_hr_id = request.user.get("hr_id")

        if not action:
            return Response(
                {"error": "Action is required (in/out)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data["entry_hr"] = user_hr_id

        # Set entry_date based on entry_start_time if it's provided
        entry_start_time = data.get("entry_start_time")
        if entry_start_time:
            data["entry_date"] = data.get("entry_date")

        serializer = JobTrackingEntrySerializer(
            data=data, context={"action": action}
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate total time before handling actions
        last_entry = (
            JobTrackingEntry.objects.filter(
                entry_hr=user_hr_id, entry_end_time__isnull=True
            )
            .order_by("-entry_start_time")
            .first()
        )

        # For clock-in action
        if action == "in":
            if last_entry:
                return Response(
                    {"message": "Already clocked in. Please clock out first."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            # Calculate total time for the new task (if applicable)
            if "entry_task_gid" in data:
                total_time = self.calculate_total_time_for_last_job(
                    user_hr_id, data["entry_task_gid"]
                )
            else:
                total_time = timedelta()  # No previous task, total time is 0

            return Response(
                {
                    "message": "Clock-in successful",
                    "time_spent": str(total_time),
                    "jobs": self.get_user_jobs_last_7_days(user_hr_id),
                },
                status=status.HTTP_201_CREATED,
            )

        # For clock-out action
        elif action == "out":
            if not last_entry:
                return Response(
                    {"message": "No active entry to clock out from."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            last_entry.entry_end_time = data.get(
                "entry_end_time", timezone.now()
            )
            last_entry.save()

            # Calculate total time for the task associated with the last entry
            total_time = self.calculate_total_time_for_last_job(
                user_hr_id, last_entry.entry_task_gid
            )

            return Response(
                {
                    "message": "Clock-out successful",
                    "time_spent": str(total_time),
                    "jobs": self.get_user_jobs_last_7_days(user_hr_id),
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "error": "Invalid action. Use 'in' to clock in or 'out' to clock out."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class JobTrackingRecentEntriesView(APIView):
    permission_classes = [JWTAuthentication]

    def get(self, request):
        # Get the current logged-in user's hr_id
        user_hr_id = request.user.get("hr_id")

        # Calculate the date 7 days ago from today
        last_7_days = timezone.now().date() - timedelta(days=7)

        # Filter JobTrackingEntry records for the logged-in user in the last 7 days
        recent_entries = JobTrackingEntry.objects.filter(
            entry_hr_id=user_hr_id, entry_date__gte=last_7_days
        )

        jobs = []

        task_time_map = {}

        for entry in recent_entries:
            if entry.entry_end_time and entry.entry_start_time:
                total_duration = entry.entry_end_time - entry.entry_start_time
                total_time_str = str(
                    total_duration
                )  # Convert duration to string format

                task_gid = entry.entry_task_gid.task_gid
                task_name = entry.entry_task_gid.task_name
                stair_category = entry.entry_task_gid.stair_category

                # Update the map with total time spent per task_gid
                if task_gid not in task_time_map:
                    task_time_map[task_gid] = {
                        "task_gid": task_gid,
                        "task_name": task_name,
                        "stair_category": stair_category,
                        "total_time": total_time_str,
                    }
                else:
                    continue

        jobs = list(task_time_map.values())

        return Response({"jobs": jobs}, status=status.HTTP_200_OK)


class UsersByTaskView(APIView):
    permission_classes = [JWTAuthentication]

    def get(self, request, task_gid):
        # Filter JobTrackingEntry for the given task_gid
        job_entries = JobTrackingEntry.objects.filter(
            entry_task_gid__task_gid=task_gid
        )

        if not job_entries.exists():
            return Response(
                {"message": "No entries found for this task."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get unique users (HumanResource) who worked on this job
        user_ids = job_entries.values_list(
            "entry_hr_id", flat=True
        ).distinct()  # Use 'entry_hr_id' to get HR IDs
        users = HumanResource.objects.filter(hr_id__in=user_ids)

        # Serialize the user data
        serializer = HumanResourceSerializer(users, many=True)

        return Response({"users": serializer.data}, status=status.HTTP_200_OK)
