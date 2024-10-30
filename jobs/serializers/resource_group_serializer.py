# jobs/serializers.py

from rest_framework import serializers
from jobs.models import ResourceGroup, ResourceGroupCategory


class ResourceGroupSerializer(serializers.ModelSerializer):
    # Use a SlugRelatedField to serialize the `group_category_name` by its name
    group_category_name = serializers.SlugRelatedField(
        queryset=ResourceGroupCategory.objects.all(),
        slug_field="group_category_name",
    )

    class Meta:
        model = ResourceGroup
        fields = [
            "group_id",
            "group_name",
            "group_parent_group",
            "group_category_name",
        ]
