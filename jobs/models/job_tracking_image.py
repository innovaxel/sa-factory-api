from django.db import models


class JobTrackingEntryImage(models.Model):
    entry_image_id = models.AutoField(
        primary_key=True, db_column="ENTRY_IMAGE_ID"
    )
    entry_id = models.ForeignKey(
        "jobs.JobTrackingEntry",
        on_delete=models.CASCADE,
        db_column="ENTRY_ID",
    )
    entry_image_url = models.TextField(db_column="ENTRY_IMAGE_URL")

    class Meta:
        db_table = "PRODUCTION_SYSTEM].[JOB_TRACKING_ENTRY_IMAGE"
        managed = True
