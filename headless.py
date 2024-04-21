import mysql

from mysql_funcs._show_tables import show_tables
from mysql_funcs._create_table import create_table
from _get_tables import get_tables
from _get_test_data import connect_to_database
import passwords as p

"""
- Get All tables in the main database
- Tables represent list names
- Select a table and show all items in table
- Table format:
    Table name---       quantity        price
        item1           3               24$
        item2           2               1$
        item3, etc.
- Can create, delete and change table names
- Can create, delete and change item names, quantity, and price
"""

#---------------------------------------------------------------------------
# Connect to database server and return cursor
cnx = mysql.connector.connect(user=p.user, password=p.password, host=p.host)
cursor = cnx.cursor()
# Connect to database
connect_to_database(cursor)

while True:

    table_list = get_tables(cursor)
    input1 = input("Enter your command:\nYou may type 'help' for commands or 'exit' to save and exit the program.\n").lower().strip()

    command_list = ['create table', 'show tables', 'delete table', 'create entry', 'show entries', 'delete entry', 'exit']
    if input1 == 'help':
        print("You may use the following commands: ")
        for command in command_list:
            print(command)

    #-----Create, Show, Delete tables
    if input1 == 'create table':
        table_name = input("Enter a name for your table")
        create_table(cursor, table_name.lower().strip().replace(' ', '_'))

    elif input1 == 'show tables':
        print("\nYour tables are as follows: \n")
        show_tables(cursor)
        print('')
        
    elif input1 == 'delete table':
        try:
            delete_table = input("Enter table to be deleted\n")
            if delete_table.lower().strip().replace(' ', '_') in table_list:
                print('Deleted')
                cursor.execute(f"DROP TABLE {delete_table.lower().strip().replace(' ','_')};")
        except:
            print('table not found')
    #-----Create, Show, Delete entries in table
    elif input1 == 'create entry':
        enter_table = input("Which table to enter: ").lower().strip().replace(' ', '_')
        fields_array = []

        # Get all fields in table
        cursor.execute(f"SHOW COLUMNS FROM {enter_table}")
        fields = cursor.fetchall()
        for field in fields:
            fields_array.append(field[0])
        
        field_values = []
        for field in fields_array:
            if field == 'item':
                value = input(f"Enter item name: ")
                field_values.append(f"'{value}'")
            if field == 'price':
                value = input(f"Enter product price: ")
                field_values.append(f"'{value}'")
            if field == 'amount':
                value = input(f"Enter quantity to be purchased: ")
                field_values.append(f"'{value}'")
        
        
        fields_data = ','.join(field_values)

        exec_string = f"INSERT IGNORE INTO {enter_table.lower().strip().replace(' ','_')} VALUES({fields_data});"
        print(exec_string)
        cursor.execute(exec_string)

    # Put this into its own function
    elif input1 == 'show entries':
        table_name = input("Enter desired table\n")
        try: 
            cursor.execute(f"SELECT * FROM {table_name};")
            f = cursor.fetchall()
            for item in f:
                print('\n')
                print("Item = ", item[0])
                print("Price = ", item[1])
                print("Quantity = ", item[2])
        except:
            print("Table not found")

    elif input1 == 'delete entry':
        try:
            table_name = input("Name of table to delete: ")
            delete_entry = input("name of entry to delete: ")
            print(table_name, delete_entry)
            cursor.execute(f"DELETE FROM {table_name} WHERE item = '{delete_entry}';")
        except:
            print("failed to delete entry")

    elif input1 == 'exit':
        cnx.commit()
        cnx.close()
        cursor.close()
        break

        

