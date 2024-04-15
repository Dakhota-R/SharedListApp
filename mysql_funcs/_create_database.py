import mysql.connector
from mysql.connector import errorcode


# pass in the cursor and new database name to create a database
def create_database(cursor, new_database):
    try:
        cursor.execute(f"CREATE DATABASE {new_database}")
        print("Database created successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"The database '{new_database}' already exists.")
        else:
            print(err._full_msg)