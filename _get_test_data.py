import mysql
import sys

import mysql.connector
from mysql_funcs._create_database import create_database
from mysql.connector import errorcode
import passwords


def connect_to_database(cursor):
    # Connect to database
    #try:
    #    create_database(cursor, "SHAREDLISTAPP")
    #except mysql.connector.Error as err:
    #    print(err._full_msg)
    # Set USE database
    try:
        cursor.execute("USE SHAREDLISTAPP;")
    except mysql.connector.Error as err:
        print(err._full_msg)
    # Return the cursor
    return cursor

def get_test_data(cursor, table):
    data_list = []
    
    try:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table}("
                    "test_val varchar(10) NOT NULL)")

        cursor.execute("INSERT INTO testing VALUES('success')")

        cursor.execute("SELECT * FROM testing;")
        data = cursor.fetchall()

        for datas in data:
            data_list.append(datas)


    except mysql.connector.Error as err:
        print(err._full_msg)
    
    return data_list

def show_tables():
    table_list = []
    try:
        cnx = mysql.connector.connect(user=passwords.user, password=passwords.password, host=passwords.host)

        cursor = cnx.cursor()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Your username or password is incorrect")
        else:
            print(err)

    cursor.execute("USE SHAREDLISTAPP")
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            table_list.append(table)


    except mysql.connector.Error as err:
        print(err._full_msg)

    return table_list