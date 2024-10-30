# jobs/views.py

from rest_framework import viewsets
from jobs.models import ResourceGroup
from jobs.serializers import ResourceGroupSerializer
from rest_framework.permissions import AllowAny


class ResourceGroupViewSet(viewsets.ModelViewSet):
    queryset = ResourceGroup.objects.all()
    serializer_class = ResourceGroupSerializer
    permission_classes = [AllowAny]
