from django.db import models


class ErrorGroupError(models.Model):
    error_group_id = models.ForeignKey(
        "jobs.ErrorGroup",
        on_delete=models.CASCADE,
        db_column="error_group_id",
    )
    error_id = models.ForeignKey(
        "jobs.Error", on_delete=models.CASCADE, db_column="error_id"
    )

    class Meta:
        db_table = "quality_system].[error_group_error"
        managed = True
        unique_together = (("error_group_id", "error_id"),)
