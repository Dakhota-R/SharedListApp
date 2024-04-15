import mysql.connector
from mysql.connector import errorcode
from mysql_funcs._show_tables import show_tables


def get_tables(cursor):
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    formatted_tables = [table[0] for table in tables]
    return formatted_tables
