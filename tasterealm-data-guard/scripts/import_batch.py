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


def to_postgres_array_literal(values: list[str]) -> str:
    escaped = []
    for item in values:
        s = str(item).replace("\\", "\\\\").replace('"', '\\"')
        escaped.append(f'"{s}"')
    return "{" + ",".join(escaped) + "}"


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
    batch_name = Path(csv_path).name

    if imported_by is None:
        imported_by = os.getenv("TR_IMPORTED_BY") or os.getenv("USER") or "import_script"

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            batch_insert_sql = """
                INSERT INTO staging.batches (batch_name, imported_by, batch_status, total_records)
                VALUES %s
                RETURNING batch_id
            """
            batch_values = [(batch_name, imported_by, "pending", len(rows))]
            inserted = execute_values(cur, batch_insert_sql, batch_values, fetch=True)
            batch_id = inserted[0][0]

            staged_insert_sql = """
                INSERT INTO staging.staged_dishes (
                    dish_name, dish_name_local, canonical_slug, primary_cuisine, course_type,
                    dish_category, meal_timing, description_short, taste_active_sweet,
                    taste_active_salty, taste_active_sour, taste_active_spicy, taste_active_umami,
                    taste_active_bitter, taste_active_overall_confidence, allergen_confidence,
                    allergen_contains_milk, allergen_contains_egg, allergen_contains_wheat,
                    allergen_contains_soy, allergen_contains_peanut, allergen_contains_tree_nut,
                    allergen_contains_fish, allergen_contains_shellfish, allergen_contains_sesame,
                    allergen_contains_gluten, diet_vegan, diet_vegetarian, diet_gluten_free,
                    diet_dairy_free, is_pork_present, is_alcohol_present, qa_status,
                    requires_manual_review, data_source, batch_id, validation_status
                )
                VALUES (
                    %(dish_name)s, %(dish_name_local)s, %(canonical_slug)s, %(primary_cuisine)s,
                    %(course_type)s, %(dish_category)s, %(meal_timing)s, %(description_short)s,
                    %(taste_active_sweet)s, %(taste_active_salty)s, %(taste_active_sour)s,
                    %(taste_active_spicy)s, %(taste_active_umami)s, %(taste_active_bitter)s,
                    %(taste_active_overall_confidence)s, %(allergen_confidence)s,
                    %(allergen_contains_milk)s, %(allergen_contains_egg)s, %(allergen_contains_wheat)s,
                    %(allergen_contains_soy)s, %(allergen_contains_peanut)s, %(allergen_contains_tree_nut)s,
                    %(allergen_contains_fish)s, %(allergen_contains_shellfish)s, %(allergen_contains_sesame)s,
                    %(allergen_contains_gluten)s, %(diet_vegan)s, %(diet_vegetarian)s,
                    %(diet_gluten_free)s, %(diet_dairy_free)s, %(is_pork_present)s,
                    %(is_alcohol_present)s, %(qa_status)s, %(requires_manual_review)s,
                    %(data_source)s, %(batch_id)s, %(validation_status)s
                )
            """

            columns_to_insert = [
                "dish_name", "dish_name_local", "canonical_slug", "primary_cuisine", "course_type",
                "dish_category", "meal_timing", "description_short", "taste_active_sweet",
                "taste_active_salty", "taste_active_sour", "taste_active_spicy", "taste_active_umami",
                "taste_active_bitter", "taste_active_overall_confidence", "allergen_confidence",
                "allergen_contains_milk", "allergen_contains_egg", "allergen_contains_wheat",
                "allergen_contains_soy", "allergen_contains_peanut", "allergen_contains_tree_nut",
                "allergen_contains_fish", "allergen_contains_shellfish", "allergen_contains_sesame",
                "allergen_contains_gluten", "diet_vegan", "diet_vegetarian", "diet_gluten_free",
                "diet_dairy_free", "is_pork_present", "is_alcohol_present", "qa_status",
                "requires_manual_review", "data_source",
            ]

            for row in rows:
                row_payload = {}
                for column in columns_to_insert:
                    value = row.get(column)
                    if pd.isna(value):
                        value = None
                    elif isinstance(value, str) and value.startswith("["):
                        value = parse_array_field(value)
                    if column == "meal_timing" and isinstance(value, list):
                        value = to_postgres_array_literal(value)
                    row_payload[column] = value

                row_payload["batch_id"] = batch_id
                row_payload["validation_status"] = "pending"
                cur.execute(staged_insert_sql, row_payload)

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# Entry point
if __name__ == "__main__":
    if len(sys.argv) not in {2, 3}:
        print("Usage: python import_batch.py <path_to_csv> [imported_by]")
        sys.exit(1)

    import_batch(sys.argv[1], imported_by=sys.argv[2] if len(sys.argv) == 3 else None)
