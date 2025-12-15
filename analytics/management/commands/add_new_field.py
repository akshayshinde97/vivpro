# Create a Python script or management command
from asyncio.windows_events import NULL

from django.core.management import BaseCommand
from django.db import connection

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "new_field",
            type=str,
            help="new field name",
        )
        parser.add_argument(
            "--new_field_type",
            type=str,
            default="VARCHAR(100)",
            help="new field type",
        )

        parser.add_argument(
            "--table",
            type=str,
            default="songs_normalized",
            help="Target SQLite table name (default: songs_normalized).",
        )

    def handle(self, *args, **options):
        table_name = options["table"]
        new_field = options["new_field"]
        new_field_type = options["new_field_type"]

        self._add_new_field(table_name, new_field, new_field_type)
    def _add_new_field(self):
        with connection.cursor() as cursor:
            cursor.execute(f" ALTER TABLE {table_name} ADD COLUMN {new_field} VARCHAR(100) NULL ")

