import json
import os

from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Normalize songs JSON and store it in db"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_path",
            type=str,
            help="Path to the JSON file (songs dataset).",
        )
        parser.add_argument(
            "--table",
            type=str,
            default="songs_normalized",
            help="Target SQLite table name (default: songs_normalized).",
        )

    def handle(self, *args, **options):
        json_path = options["json_path"]
        table_name = options["table"]

        if not os.path.exists(json_path):
            raise CommandError(f"JSON file not found: {json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict) or not data:
            raise CommandError("JSON root must be a non-empty object.")


        attributes = list(data.keys())
        print(attributes)
        first_attr = attributes[0]

        # Inner keys are indices "0", "1", ...
        indices = sorted(data[first_attr].keys(), key=lambda x: int(x))

        if not indices:
            self.stdout.write(self.style.WARNING("No rows found in JSON."))
            return

        # Optional sanity check: all attributes have same indices
        for attr in attributes:
            if set(data[attr].keys()) != set(indices):
                raise CommandError(
                    f"Attribute '{attr}' does not have the same indices as '{first_attr}'."
                )

        self.stdout.write(
            f"Found {len(attributes)} attributes and {len(indices)} rows in JSON."
        )

        # ---- Create table if it doesn't exist ----
        with connection.cursor() as cursor, transaction.atomic():
            existing_tables = connection.introspection.table_names()
            if table_name not in existing_tables:
                self._create_table(cursor, table_name, attributes, data, indices[0])
                self.stdout.write(self.style.SUCCESS(f"Created table '{table_name}'"))
            else:
                self.stdout.write(self.style.NOTICE(f"Table '{table_name}' already exists"))

            # ---- Find existing rows to avoid duplicates ----
            # We'll use the normalized index column ("idx") to detect duplicates
            cursor.execute(f'SELECT "idx" FROM "{table_name}"')
            existing_idx = {row[0] for row in cursor.fetchall()}
            self.stdout.write(f"Found {len(existing_idx)} existing rows in table.")

            # ---- Insert new rows ----
            inserted = 0
            for idx_str in indices:
                idx_int = int(idx_str)
                if idx_int in existing_idx:
                    continue  # skip duplicate

                # Build row values in the same order as columns
                row_values = [idx_int]
                for attr in attributes:
                    value = data[attr][idx_str]
                    row_values.append(value)

                columns = ['"idx"'] + [f'"{attr.lower()}"' for attr in attributes]
                placeholders = ", ".join(["%s"] * len(row_values))
                insert_sql = (
                    f'INSERT INTO "{table_name}" '
                    f'({", ".join(columns)}) VALUES ({placeholders})'
                )
                # self.stdout.write(f'SQL-{insert_sql} ---row-values--{row_values}')
                cursor.execute(insert_sql, row_values)
                inserted += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete. Inserted {inserted} new rows into '{table_name}'."
            )
        )

    def _create_table(self, cursor, table_name, attributes, data, sample_index):
        """
        Create a table with:
        - idx INTEGER PRIMARY KEY
        - one column per attribute in the JSON
        Types are inferred very simply (numbers -> REAL, else TEXT).
        """
        cols_sql = ['"idx" INTEGER PRIMARY KEY']

        for attr in attributes:
            col_name = attr.lower()
            sample_value = data[attr][sample_index]

            # Infer type in a simple way
            if isinstance(sample_value, bool):
                sql_type = "INTEGER"
            elif isinstance(sample_value, (int, float)):
                sql_type = "REAL"
            else:
                sql_type = "TEXT"

            cols_sql.append(f'"{col_name}" {sql_type}')

        create_sql = f'CREATE TABLE "{table_name}" ({", ".join(cols_sql)});'
        cursor.execute(create_sql)
