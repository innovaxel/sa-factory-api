from django.db import models
from django.utils import timezone  # Ensure this import is correct


class ErrorReport(models.Model):
    error_report_id = models.AutoField(primary_key=True)
    reported_at_department = models.ForeignKey(
        "jobs.ResourceGroup",
        on_delete=models.CASCADE,
        db_column="reported_at_department",
    )
    hr_id = models.ForeignKey(
        "accounts.HumanResource", on_delete=models.CASCADE, db_column="hr_id"
    )
    task_gid = models.ForeignKey(
        "jobs.AsanaTask", on_delete=models.CASCADE, db_column="task_gid"
    )
    reported_at_time = models.DateTimeField(
        default=timezone.now,
        db_column="reported_at_time",
    )
    comments = models.TextField(null=True, blank=True, db_column="comments")

    class Meta:
        db_table = "report_system].[error_report"
        managed = True
