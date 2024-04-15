import mysql.connector
from mysql.connector import errorcode

def enter_database(cursor, database_name):
    try:
        cursor.execute(f"USE {database_name}")
    except mysql.connector.Error as err:
        print(err._full_msg)
        return