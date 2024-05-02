import mysql.connector
from mysql.connector import errorcode

def show_tables(cursor):
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    table_list = []
    for table in tables:
        print(table[0].replace('_', ' '))
        t = table[0]
        t.replace('_', ' ')
        table_list.append(table)

    return table_list
