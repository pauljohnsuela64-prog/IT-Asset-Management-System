from database import get_connection


def get_available_assets():
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


def get_active_employees():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                employee_id,
                employee_code,
                full_name,
                department,
                position
            FROM employees
            WHERE status = 'Active'
            ORDER BY full_name
            """
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def create_assignment(
    asset_id,
    employee_id,
    assigned_date,
    notes=None,
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        connection.start_transaction()

        # Make sure the asset is still available.
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
            raise ValueError("This asset is no longer available.")

        # Make sure the employee is still active.
        cursor.execute(
            """
            SELECT status
            FROM employees
            WHERE employee_id = %s
            """,
            (employee_id,),
        )

        employee = cursor.fetchone()

        if employee is None:
            raise ValueError("Employee not found.")

        if employee["status"] != "Active":
            raise ValueError("Assets can only be assigned to active employees.")

        # Create assignment history record.
        cursor.execute(
            """
            INSERT INTO asset_assignments (
                asset_id,
                employee_id,
                assigned_date,
                status,
                notes
            )
            VALUES (%s, %s, %s, 'Assigned', %s)
            """,
            (
                asset_id,
                employee_id,
                assigned_date,
                notes,
            ),
        )

        assignment_id = cursor.lastrowid

        # Change the asset status.
        cursor.execute(
            """
            UPDATE assets
            SET status = 'Assigned'
            WHERE asset_id = %s
            """,
            (asset_id,),
        )

        connection.commit()

        return assignment_id

    except Exception:
        if connection:
            connection.rollback()

        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()