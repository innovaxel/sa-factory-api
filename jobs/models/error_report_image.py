from django.db import models


class ErrorReportImage(models.Model):
    error_report_image_id = models.AutoField(primary_key=True)
    error_report_id = models.ForeignKey(
        "jobs.ErrorReport",
        on_delete=models.CASCADE,
        db_column="error_report_id",
    )
    image_url = models.TextField(db_column="image_url")

    class Meta:
        db_table = "report_system].[error_report_image"
        managed = True
