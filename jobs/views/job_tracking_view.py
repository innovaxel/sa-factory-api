from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from jobs.models import JobTrackingEntry
from jobs.serializers import JobTrackingEntrySerializer
from django.utils import timezone


class JobTrackingView(APIView):
    def post(self, request):
        action = request.data.get("action")
        if not action:
            return Response(
                {"error": "Action is required (in/out)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = JobTrackingEntrySerializer(
            data=request.data, context={"action": action}
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        entry_hr = serializer.validated_data.get("entry_hr")

        if action == "in":
            last_entry = (
                JobTrackingEntry.objects.filter(
                    entry_hr=entry_hr, entry_end_time__isnull=True
                )
                .order_by("-entry_start_time")
                .first()
            )
            if last_entry:
                return Response(
                    {"message": "Already clocked in. Please clock out first."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save(entry_start_time=timezone.now())
            return Response(
                {"message": "Clock-in successful", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        elif action == "out":
            last_entry = (
                JobTrackingEntry.objects.filter(
                    entry_hr=entry_hr, entry_end_time__isnull=True
                )
                .order_by("-entry_start_time")
                .first()
            )
            if not last_entry:
                return Response(
                    {"message": "No active entry to clock out from."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            last_entry.entry_end_time = timezone.now()
            last_entry.save()
            serializer = JobTrackingEntrySerializer(last_entry)
            return Response(
                {"message": "Clock-out successful", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "error": "Invalid action. Use 'in' to clock in or 'out' to clock out."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
