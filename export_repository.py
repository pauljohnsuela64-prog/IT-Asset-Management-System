from database import get_connection


def get_assets_for_export():
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
                model,
                serial_number,
                status,
                purchase_date,
                notes,
                created_at
            FROM assets
            ORDER BY asset_id
            """
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def get_employees_for_export():
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
                position,
                email,
                status,
                created_at
            FROM employees
            ORDER BY employee_id
            """
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def get_assignments_for_export():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                aa.assignment_id,
                a.asset_tag,
                a.device_name,
                e.employee_code,
                e.full_name,
                e.department,
                aa.assigned_date,
                aa.returned_date,
                aa.status,
                aa.notes
            FROM asset_assignments AS aa

            INNER JOIN assets AS a
                ON aa.asset_id = a.asset_id

            INNER JOIN employees AS e
                ON aa.employee_id = e.employee_id

            ORDER BY aa.assignment_id
            """
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def get_maintenance_for_export():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                m.maintenance_id,
                a.asset_tag,
                a.device_name,
                m.maintenance_date,
                m.maintenance_type,
                m.issue_description,
                m.action_taken,
                m.technician_vendor,
                m.cost,
                m.status,
                m.completed_date,
                m.notes
            FROM maintenance_records AS m

            INNER JOIN assets AS a
                ON m.asset_id = a.asset_id

            ORDER BY m.maintenance_id
            """
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()