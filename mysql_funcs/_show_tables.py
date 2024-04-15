import mysql.connector
from mysql.connector import errorcode

def show_tables(cursor):
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    for table in tables:
        print(table[0].replace('_', ' '))
