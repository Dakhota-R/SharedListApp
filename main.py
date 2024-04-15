from tkinter import * 
import mysql



"""
- Get All tables in the main database
- Tables represent list names
- Select a table and show all items in table
- Table format:
    Table name---       quantity        price
        item1           3               24$
        item2           2               1$
        item3, etc.
"""




# My modules
from my_tk_funcs._create_button import create_button
from my_tk_funcs._create_label import create_label

import passwords

from _get_test_data import get_test_data, show_tables, connect_to_database
#---------------------------------------------------------------------------
# Connect to database server and return cursor
cnx = mysql.connector.connect(user=passwords.user, password=passwords.password, host=passwords.host)
cursor = cnx.cursor()
# Connect to database
connect_to_database(cursor)

#Init tkinter as root
root = Tk()
#-----------------------------

test_data = get_test_data(cursor, 'testing')
# Get all labels
#label_list = [create_label(root, data, index, 1) for index, data in enumerate(test_data)]
# Get list of all tables
table_list = show_tables()
for table in table_list:
    print(table[0])

#def replace_label(text, index):
    #label_list[index] = create_label(root, text, index, 1)

#lambda: replace_label('loser', 1)
#button1 = Button(root, text="Click ME!")
#button1.grid(row=10, column=10)









root.mainloop()