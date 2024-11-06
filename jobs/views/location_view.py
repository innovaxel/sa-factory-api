from rest_framework import generics
from rest_framework.response import Response
from jobs.models import Branch
from jobs.serializers import BranchSerializer
from rest_framework.permissions import AllowAny


class BranchListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "message": "Success",
                "data": serializer.data,
            }
        )
