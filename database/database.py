"""
Database Connection Module
"""

import mysql.connector
from mysql.connector import Error

from config.db_config import (
    HOST,
    PORT,
    USER,
    PASSWORD,
    DATABASE,
)


def get_connection():
    """
    Create and return a MySQL database connection.
    Returns:
        mysql.connector.connection.MySQLConnection | None
    """

    try:
        connection = mysql.connector.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
        )

        if connection.is_connected():
            return connection

    except Error as error:
        print(f"\nDatabase Connection Error:\n{error}")

    return None


def test_connection():
    """
    Test database connectivity.
    """

    connection = get_connection()

    if connection is None:
        print("\n Failed to connect to MySQL.")
        return

    print("\n Successfully connected to MySQL.")
    print(f"Database : {DATABASE}")
    print(f"Server   : {connection.get_server_info()}")

    connection.close()
    print("Connection closed.")