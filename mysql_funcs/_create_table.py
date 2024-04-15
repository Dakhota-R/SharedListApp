import mysql.connector
from mysql.connector import errorcode

from passwords import *

def create_table(cursor, table):
    print("Creating table...")
    try:
        confirm = False
        fields = []
        field_type_strings = ""
        print("Press 'Enter' when finished.")
        while confirm == False:
            print("Enter a field:")
            field = input().lower().strip().replace(' ','_')
            if field != '':
                    fields.append([field,'VARCHAR(20)'])
            else:
                confirm = True

        for i in range(0,len(fields) - 1):
            string = f"{fields[i][0]} {fields[i][1]}, "
            field_type_strings += string
        string = f"{fields[-1][0]} {fields[-1][1]}"
        field_type_strings += string

        table_string = f"CREATE TABLE IF NOT EXISTS {table}({field_type_strings})"

        cursor.execute(table_string)       
    except mysql.connector.Error as err:
        print(err._full_msg)


