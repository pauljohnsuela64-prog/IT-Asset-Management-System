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