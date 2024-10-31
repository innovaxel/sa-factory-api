# views.py
from rest_framework import generics
from rest_framework.response import Response
from jobs.models import ResourceGroup
from jobs.serializers import ResourceGroupSerializer


class ResourceGroupListView(generics.ListAPIView):
    queryset = ResourceGroup.objects.all()
    serializer_class = ResourceGroupSerializer

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "message": "Resource groups retrieved successfully.",
                "data": serializer.data,
            }
        )
