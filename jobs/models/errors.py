from django.db import models


class Error(models.Model):
    error_id = models.AutoField(primary_key=True)
    error_desc = models.TextField()
    error_department = models.IntegerField()

    class Meta:
        db_table = "QUALITY_SYSTEM].[ERROR"
