import mysql
from mysql.connector import errorcode
import mysql.connector
import mysql.connector.cursor
import sys


# My Modules
import passwords
from mysql_funcs._create_database import create_database

try:
    cnx = mysql.connector.connect(user=passwords.user, password=passwords.password, host=passwords.host)

    cursor = cnx.cursor()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Your username or password is incorrect")
    else:
        print(err)

try:
    create_database(cursor, "SHAREDLISTAPP")
except mysql.connector.Error as err:
    print(err._full_msg)

try:
    cursor.execute("USE SHAREDLISTAPP;")
    cursor.execute("CREATE TABLE IF NOT EXISTS testing("
                   "test_val varchar(10) NOT NULL)")
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    for table in tables:
        print(table)

    cursor.execute("INSERT IGNORE INTO testing VALUES('success')")
    cursor.execute("INSERT IGNORE INTO testing VALUES('derping')")

    print("RESULTS BELOW::\n")
    cursor.execute("SELECT * FROM testing;")
    data = cursor.fetchall()

    for datas in data:
        print(datas)


except mysql.connector.Error as err:
    print(err._full_msg)


def get_test_data():
    data_list = []

    try:
        cnx = mysql.connector.connect(user=passwords.user, password=passwords.password, host=passwords.host)

        cursor = cnx.cursor()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Your username or password is incorrect")
        else:
            print(err)

    try:
        create_database(cursor, "SHAREDLISTAPP")
    except mysql.connector.Error as err:
        print(err._full_msg)

    try:
        cursor.execute("USE SHAREDLISTAPP;")
        cursor.execute("CREATE TABLE IF NOT EXISTS testing("
                    "test_val varchar(10) NOT NULL)")

        cursor.execute("INSERT INTO testing VALUES('success')")
        cursor.execute("INSERT INTO testing VALUES('nerd')")

        cursor.execute("SELECT * FROM testing;")
        data = cursor.fetchall()

        for datas in data:
            data_list.append(datas)
        return data_list

    except mysql.connector.Error as err:
        print(err._full_msg)