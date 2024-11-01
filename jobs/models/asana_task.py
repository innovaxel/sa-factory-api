from django.db import models


class AsanaTask(models.Model):
    task_name = models.CharField(max_length=250)
    task_gid = models.CharField(max_length=50, unique=True, primary_key=True)
    stair_category = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.task_name} ({self.task_gid})"

    class Meta:
        managed = True
        db_table = "INTEGRATIONS].[ASANA_TASK"
