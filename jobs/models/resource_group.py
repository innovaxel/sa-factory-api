from django.db import models
from .resource_group_catrgory import ResourceGroupCategory


class ResourceGroup(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=50)
    group_parent_group = models.IntegerField(null=True, blank=True)
    group_catery_name = models.ForeignKey(
        ResourceGroupCategory,
        db_column="group_catery_name",
        on_delete=models.CASCADE,
        to_field="group_catery_name",
    )

    class Meta:
        managed = False
        db_table = "HR_SYSTEM].[RESOURCE_GROUP"
