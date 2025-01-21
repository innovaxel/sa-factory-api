from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class AdminModel(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password

    def __str__(self):
        return self.username

    class Meta:
        managed = True
        db_table = "HR_SYSTEM].[ADMINISTRATORS"
