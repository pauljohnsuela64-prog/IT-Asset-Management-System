from database import get_connection


def get_all_assets():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                asset_id,
                asset_tag,
                device_name,
                asset_type,
                brand,
                model,
                serial_number,
                status,
                purchase_date,
                created_at
            FROM assets
            ORDER BY asset_id DESC
        """)

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()