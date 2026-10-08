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


def create_asset(
    asset_tag,
    device_name,
    asset_type,
    brand,
    model=None,
    serial_number=None,
    purchase_date=None,
    notes=None,
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO assets (
                asset_tag,
                device_name,
                asset_type,
                brand,
                model,
                serial_number,
                status,
                purchase_date,
                notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, 'Available', %s, %s)
            """,
            (
                asset_tag,
                device_name,
                asset_type,
                brand,
                model,
                serial_number,
                purchase_date,
                notes,
            ),
        )

        connection.commit()
        return cursor.lastrowid

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def search_assets(search_term):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        search_value = f"%{search_term}%"

        cursor.execute(
            """
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
            WHERE asset_tag LIKE %s
               OR device_name LIKE %s
               OR asset_type LIKE %s
               OR brand LIKE %s
               OR model LIKE %s
               OR serial_number LIKE %s
               OR status LIKE %s
            ORDER BY asset_id DESC
            """,
            (
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
            ),
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()