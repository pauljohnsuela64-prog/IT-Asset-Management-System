from database import get_connection


def get_user_by_username(username):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                user_id,
                username,
                password_hash,
                role,
                status
            FROM users
            WHERE username = %s
            """,
            (username,),
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def get_all_users():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                user_id,
                username,
                role,
                status,
                created_at
            FROM users
            ORDER BY user_id DESC
            """
        )

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def create_user(
    username,
    password_hash,
    role,
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                role,
                status
            )
            VALUES (%s, %s, %s, 'Active')
            """,
            (
                username,
                password_hash,
                role,
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


def get_user_by_id(user_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                user_id,
                username,
                role,
                status,
                created_at
            FROM users
            WHERE user_id = %s
            """,
            (user_id,),
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def update_user_status(user_id, status):
    connection = None
    cursor = None

    try:
        if status not in ("Active", "Inactive"):
            raise ValueError("Invalid user status.")

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET status = %s
            WHERE user_id = %s
            """,
            (
                status,
                user_id,
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