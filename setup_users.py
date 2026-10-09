from database import get_connection


def setup_users_table():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        with open(
            "database/users.sql",
            "r",
            encoding="utf-8",
        ) as sql_file:
            sql = sql_file.read()

        cursor.execute(sql)
        connection.commit()

        print("users table is ready.")

    except Exception as error:
        print(f"Setup failed: {error}")

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    setup_users_table()