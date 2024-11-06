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

import random
import string


def generate_random_id(length=6):
    """Generate a random string of fixed length for ID."""
    return "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
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

            total_seconds = int(total_duration.total_seconds())

            formatted_time = f"{total_seconds // 3600:02}:{(total_seconds % 3600) // 60:02}:{total_seconds % 60:02}"
            return formatted_time

        return "00:00:00"

    def get_user_jobs_last_7_days(self, hr_id):

        last_7_days = timezone.now().date() - timedelta(days=7)

        recent_entries = JobTrackingEntry.objects.filter(
            entry_hr_id=hr_id, entry_date__gte=last_7_days
        )

        jobs = []
        task_time_map = {}

        for entry in recent_entries:
            if entry.entry_end_time and entry.entry_start_time:
                total_duration = entry.entry_end_time - entry.entry_start_time
                total_time_str = str(total_duration)

                task_gid = entry.entry_task_gid.task_gid
                task_name = entry.entry_task_gid.task_name
                stair_category = entry.entry_task_gid.stair_catery

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

        last_entry = (
            JobTrackingEntry.objects.filter(
                entry_hr=user_hr_id, entry_end_time__isnull=True
            )
            .order_by("-entry_start_time")
            .first()
        )

        if action == "in":
            if last_entry:
                return Response(
                    {"message": "Already clocked in. Please clock out first."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()

            if "entry_task_gid" in data:
                total_time = self.calculate_total_time_for_last_job(
                    user_hr_id, data["entry_task_gid"]
                )
            else:
                total_time = timedelta()

            return Response(
                {
                    "message": "Clock-in successful",
                    "data": {
                        "time_spent": str(total_time),
                        "jobs": self.get_user_jobs_last_7_days(user_hr_id),
                    },
                },
                status=status.HTTP_201_CREATED,
            )

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

            total_time = self.calculate_total_time_for_last_job(
                user_hr_id, last_entry.entry_task_gid
            )

            return Response(
                {
                    "message": "Clock-out successful",
                    "data": {
                        "time_spent": str(total_time),
                        "jobs": self.get_user_jobs_last_7_days(user_hr_id),
                    },
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

    def get_chip(self, obj):

        chip_mapping = {
            "External": {"color": "#73EC8B", "text": "green"},
            "REWORK": {"color": "#FF0000", "text": "red"},
            "GARAGE": {"color": "#0000FF", "text": "blue"},
            "H/R": {"color": "#CF2A45FF", "text": "pink"},
            "S/S": {"color": "#CF2A45FF", "text": "pink"},
            "SCREEN": {"color": "#FFA500", "text": "orange"},
            "SPLIT": {"color": "#FFA500", "text": "orange"},
            "STEEL TRAY": {"color": "#FFA500", "text": "orange"},
            "T-1": {"color": "#1AB338FF", "text": "green"},
            "T-2": {"color": "#1AB338FF", "text": "green"},
            "T-3": {"color": "#1AB338FF", "text": "green"},
            "T-4": {"color": "#0000FF", "text": "blue"},
            "T-5": {"color": "#0000FF", "text": "blue"},
            "T-6": {"color": "#FFA500", "text": "orange"},
            "T-7": {"color": "#FFA500", "text": "orange"},
            "T-8": {"color": "#CF2A45FF", "text": "pink"},
            "T-8-hamp": {"color": "#CF2A45FF", "text": "pink"},
            "T-9": {"color": "#FF0000", "text": "red"},
            "T-10": {"color": "#FF0000", "text": "red"},
        }

        chip_name = obj.stair_catery
        chip_data = chip_mapping.get(chip_name)

        if chip_data:
            return {
                "id": generate_random_id(),
                "color": chip_data["color"],
                "text": obj.stair_catery,
                "icon": None,
            }
        return None

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

            total_seconds = int(total_duration.total_seconds())
            formatted_time = f"{total_seconds // 3600:02}:{(total_seconds % 3600) // 60:02}:{total_seconds % 60:02}"
            return formatted_time

        return "00:00:00"

    def get(self, request):

        user_hr_id = request.user.get("hr_id")

        last_7_days = timezone.now().date() - timedelta(days=7)

        recent_entries = JobTrackingEntry.objects.filter(
            entry_hr_id=user_hr_id, entry_date__gte=last_7_days
        )

        jobs = []
        task_time_map = {}

        for entry in recent_entries:
            if entry.entry_end_time and entry.entry_start_time:
                task_gid = entry.entry_task_gid.task_gid
                task_name = entry.entry_task_gid.task_name

                total_time_str = self.calculate_total_time_for_last_job(
                    user_hr_id, task_gid
                )

                if task_gid not in task_time_map:
                    chip_data = self.get_chip(entry.entry_task_gid)

                    task_info = {
                        "id": task_gid,
                        "number": task_gid,
                        "name": task_name,
                        "total_time": total_time_str,
                        "chip": chip_data,
                        "address": {
                            "id": "ddf85998-0c53-485d-b798-072b8c59263a",
                            "address": "123 Cove Street Prahan",
                            "latitude": "0.000003",
                            "longitude": "-0.000001",
                        },
                        "customer": {
                            "id": "69bf5dac-6cb6-4f67-9a12-e1198a775f00",
                            "name": "Customer 1",
                        },
                        "status": "in_progress",
                    }
                    task_time_map[task_gid] = task_info

        jobs = list(task_time_map.values())

        return Response(
            {
                "jobs": jobs,
            },
            status=status.HTTP_200_OK,
        )


class UsersByTaskView(APIView):
    permission_classes = [JWTAuthentication]

    def get(self, request, task_gid):

        job_entries = JobTrackingEntry.objects.filter(
            entry_task_gid__task_gid=task_gid
        )

        if not job_entries.exists():
            return Response(
                {"message": "No entries found for this task."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user_ids = job_entries.values_list("entry_hr_id", flat=True).distinct()
        users = HumanResource.objects.filter(hr_id__in=user_ids)

        serializer = HumanResourceSerializer(users, many=True)

        return Response({"users": serializer.data}, status=status.HTTP_200_OK)


class CombinedJobTrackingView(APIView):
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

            total_seconds = int(total_duration.total_seconds())

            formatted_time = f"{total_seconds // 3600:02}:{(total_seconds % 3600) // 60:02}:{total_seconds % 60:02}"
            return formatted_time

        return "00:00:00"

    def get(self, request, task_gid):

        job_entries_view = JobTrackingRecentEntriesView.as_view()(
            request._request
        )
        users_view = UsersByTaskView.as_view()(
            request._request, task_gid=task_gid
        )

        user_hr_id = request.user.get("hr_id")

        combined_response = {
            "time_spent": self.calculate_total_time_for_last_job(
                user_hr_id, task_gid
            ),
            "job_id": task_gid,
            "jobs": job_entries_view.data,
            "users": users_view.data,
        }

        return Response({"data": combined_response}, status=status.HTTP_200_OK)
