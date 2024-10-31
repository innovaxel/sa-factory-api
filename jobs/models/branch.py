import uuid
from django.db import models


class Branch(models.Model):
    branch_name = models.CharField(max_length=50, primary_key=True)
    branch_guid = models.UUIDField(default=uuid.uuid4)
    # state = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = "QUOTING_SYSTEM_DB].[Branch"
