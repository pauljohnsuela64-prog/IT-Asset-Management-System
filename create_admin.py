from getpass import getpass

from werkzeug.security import generate_password_hash

from database import get_connection


def create_admin():
    connection = None
    cursor = None

    try:
        username = input("Admin username: ").strip()

        if not username:
            print("Username cannot be empty.")
            return

        password = getpass("Admin password: ")
        confirm_password = getpass("Confirm password: ")

        if not password:
            print("Password cannot be empty.")
            return

        if password != confirm_password:
            print("Passwords do not match.")
            return

        password_hash = generate_password_hash(password)

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
            VALUES (%s, %s, 'Admin', 'Active')
            """,
            (
                username,
                password_hash,
            ),
        )

        connection.commit()

        print("Admin account created successfully.")

    except Exception as error:
        if connection:
            connection.rollback()

        print(f"Unable to create admin: {error}")

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    create_admin()