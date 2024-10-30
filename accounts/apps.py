# accounts/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db import connection


def create_schema(schema_name):
    """Utility function to create a schema if it doesn't exist in SQL Server."""
    with connection.cursor() as cursor:
        # SQL Server syntax to conditionally create a schema
        cursor.execute(
            f"""
            IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = '{schema_name}')
            BEGIN
                EXEC('CREATE SCHEMA {schema_name}')
            END
        """
        )


def create_schemas(sender, **kwargs):
    """Function to create necessary schemas after migrations."""
    create_schema("quotingsyste")


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Connect the post_migrate signal to create schemas only after migrations
        post_migrate.connect(create_schemas, sender=self)
