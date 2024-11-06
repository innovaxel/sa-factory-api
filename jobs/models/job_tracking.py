from django.db import models


from .resource_group import ResourceGroup


class JobTrackingEntry(models.Model):
    entry_id = models.AutoField(primary_key=True)
    entry_date = models.DateField(null=False, blank=False)
    entry_branch_name = models.ForeignKey(
        "jobs.Branch",
        on_delete=models.CASCADE,
        db_column="ENTRY_BRANCH_NAME",
        related_name="job_tracking_entries",
    )
    entry_area_group = models.ForeignKey(
        ResourceGroup,
        on_delete=models.CASCADE,
        db_column="ENTRY_AREA_GROUP_ID",
        related_name="job_tracking_entries",
    )
    entry_hr = models.ForeignKey(
        "accounts.HumanResource",
        on_delete=models.CASCADE,
        db_column="ENTRY_HR_ID",
        related_name="job_tracking_entries",
    )
    entry_task_gid = models.ForeignKey(
        "jobs.AsanaTask",
        on_delete=models.CASCADE,
        db_column="ENTRY_TASK_GID",
        to_field="task_gid",  # Reference the task_gid field
        related_name="job_tracking_entries",
    )
    entry_job_id = models.IntegerField(null=True, blank=True)
    entry_start_time = models.DateTimeField(null=True, blank=True)
    entry_end_time = models.DateTimeField(null=True, blank=True)
    entry_comment = models.TextField(null=True, blank=True)
    entry_is_complete = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "PRODUCTION_SYSTEM].[JOB_TRACKING_ENTRY"

    def __str__(self):
        return f"Entry {self.entry_id} for Task {self.entry_task_gid}"
