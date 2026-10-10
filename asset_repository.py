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

def get_asset_by_id(asset_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM assets
            WHERE asset_id = %s
            """,
            (asset_id,),
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def update_asset(
    asset_id,
    asset_tag,
    device_name,
    asset_type,
    brand,
    model,
    serial_number,
    status,
    purchase_date,
    notes,
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE assets
            SET asset_tag = %s,
                device_name = %s,
                asset_type = %s,
                brand = %s,
                model = %s,
                serial_number = %s,
                status = %s,
                purchase_date = %s,
                notes = %s
            WHERE asset_id = %s
            """,
            (
                asset_tag,
                device_name,
                asset_type,
                brand,
                model,
                serial_number,
                status,
                purchase_date,
                notes,
                asset_id,
            ),
        )

        connection.commit()
        return cursor.rowcount

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def retire_asset(asset_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        connection.start_transaction()

        cursor.execute(
            """
            SELECT status
            FROM assets
            WHERE asset_id = %s
            FOR UPDATE
            """,
            (asset_id,),
        )

        asset = cursor.fetchone()

        if asset is None:
            raise ValueError("Asset not found.")

        if asset["status"] == "Assigned":
            raise ValueError(
                "Assigned assets must be returned before they can be retired."
            )

        if asset["status"] == "Retired":
            raise ValueError("This asset is already retired.")

        cursor.execute(
            """
            UPDATE assets
            SET status = 'Retired'
            WHERE asset_id = %s
            """,
            (asset_id,),
        )

        connection.commit()

        return cursor.rowcount

    except Exception:
        if connection:
            connection.rollback()

        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def asset_has_history(asset_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM asset_assignments
            WHERE asset_id = %s
            """,
            (asset_id,),
        )

        assignment_count = cursor.fetchone()["count"]

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM maintenance_records
            WHERE asset_id = %s
            """,
            (asset_id,),
        )

        maintenance_count = cursor.fetchone()["count"]

        return assignment_count > 0 or maintenance_count > 0

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def delete_asset(asset_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM assets
            WHERE asset_id = %s
            """,
            (asset_id,),
        )

        connection.commit()

        return cursor.rowcount

    except Exception:
        if connection:
            connection.rollback()

        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()