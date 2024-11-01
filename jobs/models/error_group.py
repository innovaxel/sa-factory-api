from django.db import models


class ErrorGroup(models.Model):
    error_group_id = models.AutoField(primary_key=True)
    error_group_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "QUALITY_SYSTEM].[ERROR_GROUP"
