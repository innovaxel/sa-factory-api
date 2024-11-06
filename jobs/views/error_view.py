from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from jobs.models import ErrorGroup
from jobs.serializers import ErrorGroupSerializer


class ErrorGroupListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            error_groups = ErrorGroup.objects.all()
            serializer = ErrorGroupSerializer(error_groups, many=True)
            return Response(
                {
                    "message": "Data retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "message": "An error occurred",
                    "data": None,
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
