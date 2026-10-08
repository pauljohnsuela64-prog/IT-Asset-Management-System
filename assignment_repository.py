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


def get_all_assignments():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                aa.assignment_id,
                aa.assigned_date,
                aa.returned_date,
                aa.status,
                aa.notes,

                a.asset_tag,
                a.device_name,
                a.asset_type,

                e.employee_code,
                e.full_name,
                e.department

            FROM asset_assignments AS aa

            INNER JOIN assets AS a
                ON aa.asset_id = a.asset_id

            INNER JOIN employees AS e
                ON aa.employee_id = e.employee_id

            ORDER BY aa.assignment_id DESC
            """
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def get_assignment_by_id(assignment_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                aa.assignment_id,
                aa.asset_id,
                aa.employee_id,
                aa.assigned_date,
                aa.returned_date,
                aa.status,
                aa.notes,

                a.asset_tag,
                a.device_name,

                e.employee_code,
                e.full_name

            FROM asset_assignments AS aa

            INNER JOIN assets AS a
                ON aa.asset_id = a.asset_id

            INNER JOIN employees AS e
                ON aa.employee_id = e.employee_id

            WHERE aa.assignment_id = %s
            """,
            (assignment_id,),
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def return_assignment(assignment_id, returned_date):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        connection.start_transaction()

        cursor.execute(
            """
            SELECT
                asset_id,
                status
            FROM asset_assignments
            WHERE assignment_id = %s
            FOR UPDATE
            """,
            (assignment_id,),
        )

        assignment = cursor.fetchone()

        if assignment is None:
            raise ValueError("Assignment not found.")

        if assignment["status"] != "Assigned":
            raise ValueError("This asset has already been returned.")

        asset_id = assignment["asset_id"]

        cursor.execute(
            """
            UPDATE asset_assignments
            SET returned_date = %s,
                status = 'Returned'
            WHERE assignment_id = %s
            """,
            (
                returned_date,
                assignment_id,
            ),
        )

        cursor.execute(
            """
            UPDATE assets
            SET status = 'Available'
            WHERE asset_id = %s
            """,
            (asset_id,),
        )

        connection.commit()

    except Exception:
        if connection:
            connection.rollback()

        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()