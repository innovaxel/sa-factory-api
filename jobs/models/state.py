from django.db import models


class State(models.Model):
    """
    Represents a state with its name, phone code, and abbreviation.

    Attributes:
        state_name (str): The name of the state, must be unique and cannot be null.
        state_phone_code (str): The phone code of the state, can be null.
        state_abbr (str): The abbreviation of the state, can be null.
    """

    state_name = models.CharField(max_length=30, primary_key=True)
    state_phone_code = models.CharField(max_length=2, blank=True, null=True)
    state_abbr = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "QUOTING_SYSTEM_DB].[STATE"

    def __str__(self):
        return str(self.state_name)
