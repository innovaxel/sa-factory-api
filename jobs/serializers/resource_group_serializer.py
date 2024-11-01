import random
from rest_framework import serializers
from accounts.models import HumanResource
from jobs.models import ResourceGroup, ResourceGroupCategory
from accounts.serializers import HumanResourceSerializer


class ResourceGroupCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceGroupCategory
        fields = ["group_category_name"]


class ResourceGroupSerializer(serializers.ModelSerializer):
    group_category_name = ResourceGroupCategorySerializer()
    users = serializers.SerializerMethodField()
    location_id = serializers.SerializerMethodField()

    class Meta:
        model = ResourceGroup
        fields = [
            "id",
            "title",
            "location_id",
            "worklist_parent",
            "group_category_name",
            "users",
        ]

    id = serializers.CharField(source="group_id")
    title = serializers.CharField(source="group_name")
    worklist_parent = serializers.IntegerField(source="group_parent_group")
    group_category_name = serializers.CharField(
        source="group_category_name.group_category_name"
    )

    def get_users(self, obj):
        all_users = HumanResource.objects.all()
        return HumanResourceSerializer(all_users, many=True).data

    def get_location_id(self, obj):
        """Return the role for the human resource."""
        return str(random.randint(10000, 99999))  # Return a string directly
