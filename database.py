import os
from pathlib import Path
from urllib.parse import unquote, urlsplit

import mysql.connector
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().with_name(".env"))


def get_database_config():
    """Choose one credential source and validate the intended database."""
    local_keys = ("DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME")
    railway_keys = ("MYSQLHOST", "MYSQLPORT", "MYSQLUSER", "MYSQLPASSWORD", "MYSQLDATABASE")
    if any(os.getenv(key) is not None for key in local_keys):
        keys = local_keys
    elif any(os.getenv(key) is not None for key in railway_keys):
        keys = railway_keys
    else:
        keys = None

    if keys:
        host, port, user, password, name = (os.getenv(key) for key in keys)
        config = dict(host=host, port=port or "3306", user=user, password=password, database=name)
    elif os.getenv("MYSQL_URL"):
        try:
            url = urlsplit(os.environ["MYSQL_URL"])
            if url.scheme != "mysql" or url.query or url.fragment:
                raise ValueError
            config = dict(
                host=url.hostname,
                port=url.port or 3306,
                user=unquote(url.username or ""),
                password=unquote(url.password) if url.password is not None else None,
                database=unquote(url.path.removeprefix("/")),
            )
        except ValueError:
            raise ValueError("MYSQL_URL must be a valid mysql:// connection URL without query parameters.") from None
    else:
        raise ValueError("Configure DB_* variables or Railway MYSQL* variables / MYSQL_URL.")

    if any(not config[field] for field in ("host", "user", "database")) or config["password"] is None:
        raise ValueError("Database configuration is incomplete; use one complete credential source.")
    try:
        config["port"] = int(config["port"])
        if not 1 <= config["port"] <= 65535:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError("Database port must be an integer between 1 and 65535.") from None

    expected_name = os.getenv("DB_EXPECTED_NAME", "it_asset_management")
    if not expected_name or config["database"] != expected_name:
        raise ValueError("Database name does not match DB_EXPECTED_NAME (default: it_asset_management). Connection refused.")
    return config


def get_connection():
    return mysql.connector.connect(**get_database_config())
