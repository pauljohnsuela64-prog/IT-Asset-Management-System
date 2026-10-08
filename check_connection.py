from database import get_connection


try:
    connection = get_connection()

    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE(), 1")
    database_name, result = cursor.fetchone()

    print(f"Connection successful.")
    print(f"Database: {database_name}")
    print(f"MySQL answered: {result}")

    cursor.close()
    connection.close()

except Exception as error:
    print(f"Connection failed: {error}")