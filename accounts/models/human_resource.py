import uuid
from django.db import models

from .contact import Contact
from jobs.models import Branch


class HumanResource(models.Model):
    hr_id = models.AutoField(primary_key=True)
    hr_job_title = models.CharField(max_length=100)
    contact_id = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        db_column="contact_id",  # Custom column name
    )
    hr_supervisor_id = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subordinates",
        db_column="hr_supervisor_id",  # Custom column name
    )
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column="branch_name",  # Custom column name
    )
    hr_guid = models.UUIDField(default=uuid.uuid4)
    hr_pin = models.CharField(max_length=32, null=True, blank=True)
    hr_timesheet_user = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hr_job_title} - {self.hr_guid}"

    class Meta:
        managed = True
        db_table = "HR_SYSTEM].[HUMAN_RESOURCE"
