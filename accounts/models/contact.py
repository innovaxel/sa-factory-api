from django.db import models


class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_first_name = models.CharField(max_length=255)
    contact_last_name = models.CharField(max_length=255, null=True, blank=True)
    contact_pref_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return (
            f"{self.contact_first_name} {self.contact_last_name or ''}".strip()
        )

    class Meta:
        managed = True
        db_table = "QUOTING_SYSTEM_DB].[CONTACT"
