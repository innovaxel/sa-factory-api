# serializers.py
from rest_framework import serializers
from jobs.models import ResourceGroup, ResourceGroupCategory


class ResourceGroupCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceGroupCategory
        fields = ["group_category_name"]


class ResourceGroupSerializer(serializers.ModelSerializer):
    group_category_name = (
        ResourceGroupCategorySerializer()
    )  # Nesting the category serializer

    class Meta:
        model = ResourceGroup
        fields = [
            "group_id",
            "group_name",
            "group_parent_group",
            "group_category_name",
        ]
