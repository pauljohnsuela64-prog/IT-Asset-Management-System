from database import get_connection


def get_all_employees():
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
            ORDER BY employee_id DESC
            """
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def create_employee(
    employee_code,
    full_name,
    department,
    position=None,
    email=None,
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO employees (
                employee_code,
                full_name,
                department,
                position,
                email,
                status
            )
            VALUES (%s, %s, %s, %s, %s, 'Active')
            """,
            (
                employee_code,
                full_name,
                department,
                position,
                email,
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


def search_employees(search_term):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        search_value = f"%{search_term}%"

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
            WHERE employee_code LIKE %s
               OR full_name LIKE %s
               OR department LIKE %s
               OR position LIKE %s
               OR email LIKE %s
               OR status LIKE %s
            ORDER BY employee_id DESC
            """,
            (
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