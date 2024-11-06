from django.db import models


class ResourceGroupCategory(models.Model):
    group_catery_name = models.CharField(max_length=50, primary_key=True)

    class Meta:
        managed = False
        db_table = "HR_SYSTEM].[RESOURCE_GROUP_CATERY"
