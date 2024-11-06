from rest_framework import viewsets, status
from rest_framework.response import Response
from common.auth import JWTAuthentication
from jobs.serializers import ErrorReportCreateSerializer, ErrorReportSerializer


class ErrorReportViewSet(viewsets.ViewSet):
    permission_classes = [JWTAuthentication]

    def create(self, request):
        try:

            user_hr_id = request.user.get("hr_id")

            if user_hr_id is None:
                return Response(
                    {
                        "message": "User HR ID not found in the token",
                        "data": None,
                        "error": "Authentication error",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            request.data["hr_id"] = user_hr_id

            serializer = ErrorReportCreateSerializer(data=request.data)
            if serializer.is_valid():

                error_report = serializer.save()

                response_serializer = ErrorReportSerializer(error_report)

                return Response(
                    {
                        "message": "Error report created successfully",
                        "data": response_serializer.data,
                        "error": None,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:

                return Response(
                    {
                        "message": "Error report creation failed",
                        "data": None,
                        "error": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:

            return Response(
                {
                    "message": "An unexpected error occurred",
                    "data": None,
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
