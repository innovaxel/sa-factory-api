from django.db import models, connection


class Branch(models.Model):
    branch_name = models.CharField(max_length=50, primary_key=True)
    branch_guid = models.UUIDField(null=True, default=None)
    state = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = "branch"
        verbose_name_plural = "Branches"
