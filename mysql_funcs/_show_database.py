import mysql.connector
from mysql.connector import errorcode

def show_databases(cursor):
    print("Your current databases are: \n")
    cursor.execute("SHOW DATABASES;")
    result = cursor.fetchall()
    for db in result:
        print(db)