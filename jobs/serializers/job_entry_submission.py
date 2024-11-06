# # serializers.py
# from rest_framework import serializers
# from .models import JobTrackingEntry, JobTrackingEntryImage
# from jobs.models import Branch, AsanaTask
# from accounts.models import HumanResource
# from .resource_group import ResourceGroup


# class JobTrackingEntryImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = JobTrackingEntryImage
#         fields = ["entry_image_url"]


# class JobTrackingEntrySerializer(serializers.ModelSerializer):
#     images = serializers.ListField(
#         child=serializers.URLField(), write_only=True, required=False
#     )

#     class Meta:
#         model = JobTrackingEntry
#         fields = [
#             "entry_date",
#             "entry_branch_name",
#             "entry_area_group",
#             "entry_hr",
#             "entry_task_gid",
#             "entry_start_time",
#             "entry_comment",
#             "entry_is_complete",
#             "images",
#         ]

#     def create(self, validated_data):
#         images = validated_data.pop("images", [])

#         # Retrieve and set foreign key instances
#         branch_id = validated_data.pop("entry_branch_name")
#         area_group_id = validated_data.pop("entry_area_group")
#         hr_id = validated_data.pop("entry_hr")
#         task_gid = validated_data.pop("entry_task_gid")

#         entry_branch_name = Branch.objects.get(pk=branch_id)
#         entry_area_group = ResourceGroup.objects.get(pk=area_group_id)
#         entry_hr = HumanResource.objects.get(pk=hr_id)
#         entry_task_gid = AsanaTask.objects.get(task_gid=task_gid)

#         # Create the JobTrackingEntry instance
#         job_entry = JobTrackingEntry.objects.create(
#             entry_branch_name=entry_branch_name,
#             entry_area_group=entry_area_group,
#             entry_hr=entry_hr,
#             entry_task_gid=entry_task_gid,
#             **validated_data
#         )

#         # Create associated images
#         for image_url in images:
#             JobTrackingEntryImage.objects.create(
#                 entry_id=job_entry, entry_image_url=image_url
#             )

#         return job_entry


from rest_framework import serializers
from accounts.models.human_resource import HumanResource
from jobs.models import JobTrackingEntry, Branch, ResourceGroup, AsanaTask


class JobEntrySubmissionSerializer(serializers.ModelSerializer):
    entry_branch_name = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all()
    )
    entry_area_group = serializers.PrimaryKeyRelatedField(
        queryset=ResourceGroup.objects.all()
    )
    entry_hr = serializers.PrimaryKeyRelatedField(
        queryset=HumanResource.objects.all()
    )
    entry_task_gid = serializers.PrimaryKeyRelatedField(
        queryset=AsanaTask.objects.all()
    )
    entry_start_time = serializers.DateTimeField(required=False)

    class Meta:
        model = JobTrackingEntry
        fields = [
            "entry_date",
            "entry_branch_name",
            "entry_area_group",
            "entry_hr",
            "entry_task_gid",
            "entry_comment",
            "entry_is_complete",
            "entry_start_time",  # Include this field
        ]
