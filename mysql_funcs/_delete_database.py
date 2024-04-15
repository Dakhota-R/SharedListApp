import mysql.connector
from mysql.connector import errorcode

def delete_database(cursor, database):
    try:
        cursor.execute(f"DROP DATABASE {database}")
        print(f"Database {database} deleted successfully.")
    except mysql.connector.Error as err:
        print(err._full_msg)