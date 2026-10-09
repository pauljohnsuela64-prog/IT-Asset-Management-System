from database import get_connection


def get_all_maintenance_records():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                m.maintenance_id,
                m.maintenance_date,
                m.maintenance_type,
                m.issue_description,
                m.action_taken,
                m.technician_vendor,
                m.cost,
                m.status,
                m.completed_date,
                m.notes,

                a.asset_id,
                a.asset_tag,
                a.device_name,
                a.asset_type,
                a.brand,
                a.model

            FROM maintenance_records AS m

            INNER JOIN assets AS a
                ON m.asset_id = a.asset_id

            ORDER BY m.maintenance_id DESC
            """
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def get_maintainable_assets():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                asset_id,
                asset_tag,
                device_name,
                asset_type,
                brand,
                model
            FROM assets
            WHERE status = 'Available'
            ORDER BY asset_tag
            """
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def create_maintenance_record(
    asset_id,
    maintenance_date,
    maintenance_type,
    issue_description,
    technician_vendor=None,
    cost=0,
    notes=None,
):
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

        if asset["status"] != "Available":
            raise ValueError(
                "Only available assets can be placed under maintenance."
            )

        cursor.execute(
            """
            INSERT INTO maintenance_records (
                asset_id,
                maintenance_date,
                maintenance_type,
                issue_description,
                technician_vendor,
                cost,
                status,
                notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, 'Open', %s)
            """,
            (
                asset_id,
                maintenance_date,
                maintenance_type,
                issue_description,
                technician_vendor,
                cost,
                notes,
            ),
        )

        maintenance_id = cursor.lastrowid

        cursor.execute(
            """
            UPDATE assets
            SET status = 'Under Maintenance'
            WHERE asset_id = %s
            """,
            (asset_id,),
        )

        connection.commit()

        return maintenance_id

    except Exception:
        if connection:
            connection.rollback()

        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()