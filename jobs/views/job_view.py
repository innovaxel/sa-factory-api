from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.auth import JWTAuthentication
from jobs.models import AsanaTask
from jobs.serializers import AsanaTaskSerializer


class AsanaTaskListView(APIView):
    permission_classes = [JWTAuthentication]

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
    permission_classes = [JWTAuthentication]

    def get(self, request, worklist_id):
        tasks = AsanaTask.objects.all()
        serializer = AsanaTaskSerializer(tasks, many=True)
        return Response(
            {
                "message": "Success",
                "data": {
                    "worklist_id": worklist_id,
                    "jobs": serializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )
