from database import get_connection


def get_dashboard_stats():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        stats = {}

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM assets
            """
        )
        stats["total_assets"] = cursor.fetchone()["count"]

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM assets
            WHERE status = 'Available'
            """
        )
        stats["available_assets"] = cursor.fetchone()["count"]

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM assets
            WHERE status = 'Assigned'
            """
        )
        stats["assigned_assets"] = cursor.fetchone()["count"]

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM assets
            WHERE status = 'Under Maintenance'
            """
        )
        stats["maintenance_assets"] = cursor.fetchone()["count"]

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM assets
            WHERE status = 'Retired'
            """
        )
        stats["retired_assets"] = cursor.fetchone()["count"]

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM employees
            WHERE status = 'Active'
            """
        )
        stats["active_employees"] = cursor.fetchone()["count"]

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM asset_assignments
            WHERE status = 'Assigned'
            """
        )
        stats["active_assignments"] = cursor.fetchone()["count"]

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM maintenance_records
            WHERE status != 'Completed'
            """
        )
        stats["open_maintenance"] = cursor.fetchone()["count"]

        return stats

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()