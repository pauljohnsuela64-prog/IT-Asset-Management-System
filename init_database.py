"""Manually create missing tables without deleting data or migrating schemas."""
from pathlib import Path
import sys

from database import get_connection


SCHEMA_FILES = (
    "assets.sql",
    "employees.sql",
    "asset_assignments.sql",
    "maintenance_records.sql",
    "users.sql",
)


def initialize_database():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        for filename in SCHEMA_FILES:
            sql = (Path(__file__).resolve().parent / "database" / filename).read_text(encoding="utf-8")
            cursor.execute(sql)
            connection.commit()
            print(f"Ready: {filename.removesuffix('.sql')}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    try:
        initialize_database()
    except Exception:
        # Driver errors can contain connection details; do not print credentials.
        print("Database initialization failed. Check configuration, connectivity, and schema privileges. Earlier table creation may have committed; fix the cause before retrying.", file=sys.stderr)
        sys.exit(1)
