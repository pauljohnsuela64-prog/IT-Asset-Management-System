import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    database_name = os.getenv("DB_NAME")

    if database_name != "it_asset_management":
        raise ValueError(
            "DB_NAME must be exactly 'it_asset_management'. Connection refused."
        )

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=database_name,
    )