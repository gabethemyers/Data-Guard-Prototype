import ast
import os
import sys
import uuid
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values


def parse_array_field(value: str) -> list[str] | str:
    """
    Parses a JSON/Python-style array string from a CSV cell into a list.
    Returns the original value unchanged if it is not array-shaped,
    so scalar fields pass through safely.
    """
    if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            # Return raw string — the validator will flag it as malformed
            return value
    return value


def get_connection():
    return psycopg2.connect(
        host=os.getenv("TR_DB_HOST", "localhost"),
        port=int(os.getenv("TR_DB_PORT", "5432")),
        dbname=os.getenv("TR_DB_NAME", "tasterealm_dev"),
        user=os.getenv("TR_DB_USER", "gabriel"),
        password=os.getenv("TR_DB_PASSWORD", "devpassword123"),
    )


def get_table_columns(cursor, schema: str, table: str) -> set[str]:
    cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s
          AND table_name = %s
        """,
        (schema, table),
    )
    return {row[0] for row in cursor.fetchall()}


def import_batch(csv_path: str, imported_by: str | None = None) -> None:
    df = pd.read_csv(csv_path)
    rows = df.to_dict(orient='records')


# Entry point
if __name__ == "__main__":
    if len(sys.argv) not in {2, 3}:
        print("Usage: python import_batch.py <path_to_csv> [imported_by]")
        sys.exit(1)

    import_batch(sys.argv[1], imported_by=sys.argv[2] if len(sys.argv) == 3 else None)
