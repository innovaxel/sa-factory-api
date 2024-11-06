from django.db import models


class ErrorReportError(models.Model):
    error_report_id = models.ForeignKey(
        "jobs.ErrorReport",
        on_delete=models.CASCADE,
        db_column="error_report_id",
    )
    error_id = models.ForeignKey(
        "jobs.Error", on_delete=models.CASCADE, db_column="error_id"
    )

    class Meta:
        db_table = "report_system].[error_report_error"
        managed = True
        unique_together = (("error_report_id", "error_id"),)
