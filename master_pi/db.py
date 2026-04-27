import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="piot_db"
        )
    except Error as error:
        print(f"Database connection failed: {error}")
        return None