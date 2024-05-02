from tkinter import *
import customtkinter as ctk
import mysql
from mysql.connector import errorcode
import mysql.connector

import passwords

my_font = ('Helvetica', 30, 'bold')

try:
    cnx = mysql.connector.connect(user=passwords.user, password=passwords.password, host=passwords.host)

    cursor = cnx.cursor()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Your username or password is incorrect")
    else:
        print(err)


try:
    cursor.execute('USE SHAREDLISTAPP;')
except mysql.connector.Error as err:
    print(err._full_msg)

# get tables
db_tables = {}
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()
for table in tables:
    table_name = list(table)[0]


    items_list = []
    cursor.execute(f'SELECT * FROM {table_name};')
    items = cursor.fetchall()

    fields_list = []
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    fields = cursor.fetchall()

    for field in fields:
        fields_list.append(list(field)[0])

    items_list = []
    for item in items:
        cur_item = list(item)
        item_vals = {}
        for index, val in enumerate(cur_item):
            ci_field = list(fields[index])
            ci = ci_field[0] 
            item_vals[ci] = val
        
        items_list.append(item_vals)
    
    items_fields = {}
    items_fields['Items'] = items_list
    items_fields['Fields'] = fields_list
    db_tables[table_name] = items_fields

print(db_tables)


def create_table(table, fields):
    print('creating table...')
    fields_list = []

    for field in fields:
        print(field)
        field_string = f'{field} VARCHAR(20)'
        fields_list.append(field_string)

    fields_string = ', '.join(fields_list)
    
    exec_string = f"CREATE TABLE IF NOT EXISTS {table} ({fields_string});"

    cursor.execute(exec_string)

def set_entries(table, entries, fields):
    print(f'Setting values in table: {table}...')

    fields_string = ', '.join(fields)

    formatted_entries = []
    for entry in entries:
        formatted_entry = f"'{entry}'"
        formatted_entries.append(formatted_entry)

    entry_string = ', '.join(formatted_entries)

    print(entry_string)

    exec_string = f"INSERT IGNORE INTO {table} ({fields_string}) VALUES ({entry_string});"
    print(exec_string)
    cursor.execute(exec_string)
    cnx.commit()

def delete_table(table):
    cursor.execute(f"DROP TABLE {table}")
    cnx.commit()

def delete_entry(table, field, entry):
    cursor.execute(f"DELETE FROM {table} WHERE {field}='{entry}';")
    cnx.commit()




class AddTableWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.minsize(350, 100)
        self.grab_set()

        self.wrapper = ctk.CTkFrame(self)
        self.wrapper.pack(expand='y', fill='both')

        label = ctk.CTkLabel(self.wrapper, text='Enter list name: ', width = 20)
        label.pack()
        self.namebox = ctk.CTkTextbox(self.wrapper, height=12, width = 150)
        self.namebox.pack()
        submit_button = ctk.CTkButton(self.wrapper, text='submit', width=200, command=self.fields_window)
        submit_button.pack()
        
    def fields_window(self):
        try:
            self.name_input = self.namebox.get("1.0","end-1c").strip()
        except:
            self.name_input = 'List'
        
        for child in self.wrapper.winfo_children():
            child.destroy()

        self.label = ctk.CTkLabel(self.wrapper, text=self.name_input)
        self.label.pack()

        self.fields_frame = ctk.CTkScrollableFrame(self.wrapper, height=100)
        # ctk bug fix for scrollframe height:
        self.fields_frame._scrollbar.configure(height=0)
        self.fields_frame.pack()

        self.fields_list = {}

        #field button and input frame
        field_input_frame = ctk.CTkFrame(self)
        field_input_frame.pack(expand='n', fill='x')
        self.add_field_text = ctk.CTkTextbox(field_input_frame, height=12)
        self.add_field_text.pack(side='left', anchor='w')
        add_field_btn = ctk.CTkButton(field_input_frame, text='add field', command=self.add_field)
        add_field_btn.pack()
        submit_button = ctk.CTkButton(self, text='Submit', command=self.submit_table)
        submit_button.pack(fill='x')

    def add_field(self):
        field=self.add_field_text.get("1.0","end-1c").strip().lower()
        if field and field not in self.fields_list:
            self.add_field_text.delete("1.0", END)
            
            field_card = ctk.CTkFrame(self.fields_frame)
            field_card.pack(fill='x')
            field_label = ctk.CTkLabel(field_card, text=field)
            field_label.pack(side='left', anchor='w')
            delete_field_btn = ctk.CTkButton(field_card, text='X', width=23, command=lambda i = field_card, j = field: self.destroy_field(i, j))
            delete_field_btn.pack(side='right', anchor='e')

            self.fields_list[field] = field_card

        #print(self.fields_list)

    def destroy_field(self, i, j):
        i.destroy()
        del self.fields_list[j]
        #print(len(self.fields_list))


    def submit_table(self):
        self.entry_name = self.name_input
        self.entry_items = []
        for field in self.fields_list:
            self.entry_items.append(field)

        create_table(self.entry_name.strip(), self.entry_items)

        items_fields = {}
        items_fields['Fields'] = self.entry_items
        items_fields['Items'] = []

        db_tables[self.entry_name] = items_fields
        #print(db_tables[self.entry_name])
        #AddItemWindow.get_fields(AddItemWindow, self.entry_items)
        AllListsFrame.show_lists(app.frames['AllListsFrame'])
        self.destroy()
        


#---------------------------------------------------------------------------------------------------------------------------------------
class AddItemWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.label = ctk.CTkLabel(self, text= 'Add new item')
        self.label.pack()

        self.wrapper = ctk.CTkFrame(self)
        self.wrapper.pack()

        self.show_field_entries()

        self.confirm_button = ctk.CTkButton(self, text='confirm', command=self.send_input)
        self.confirm_button.pack()

        self.minsize(300,100)
        self.grab_set()
        


    def show_field_entries(self):
        self.fields_list = []
        ShowListFrame.destroy_items_in_items_frame(app.frames['ShowListFrame'])
        self.current_table = app.frames['ShowListFrame'].table
        print(self.current_table, '<-- current table')
        ShowListFrame.set_table(app.frames['ShowListFrame'], self.current_table)
        
        for field in db_tables[self.current_table]['Fields']:
            if field not in self.fields_list:
                self.fields_list.append(field)
        
        
        for child in self.wrapper.winfo_children():
            child.destroy()

        self.field_cards = []
        for field in self.fields_list:
            frame = ctk.CTkFrame(self.wrapper)
            frame.pack()
            label = ctk.CTkLabel(frame, text=f"Enter {field}")
            label.pack(side='left', anchor='w')
            frame.textinput = ctk.CTkTextbox(frame, width=100, height=12)
            frame.textinput.pack()
            self.field_cards.append(frame)

        ShowListFrame.create_item_list(app.frames['ShowListFrame'], ShowListFrame.table_list)

    def send_input(self):
        values = []
        for frame in self.field_cards:
            val = frame.textinput.get("1.0", "end-1c")
            values.append(val)

        #print(values, fields)
        ShowListFrame.add_item(app.frames['ShowListFrame'], values, self.fields_list)
        ShowListFrame.create_item_list(app.frames['ShowListFrame'], ShowListFrame.table_list)
        set_entries(self.current_table, values, self.fields_list)
        self.destroy()

#---------------------------------------------------------------------------------------------------------------------------------------
class AllListsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.controller = controller
        self.parent = parent
        
        self.input_box = None

        label = ctk.CTkLabel(self, text='My List App')
        label.pack()

        create_list_button = ctk.CTkButton(self, text='Create New List', command=self.open_input_box)
        create_list_button.pack()

        self.tables_frame = ctk.CTkScrollableFrame(self, width=400)
        self.tables_frame.pack(fill='both', expand='y', side='top')

        x = None

        self.list_list = []

        self.show_lists()

            
    def show_lists(self):
        for child in self.tables_frame.winfo_children():
            child.destroy()
        for table in db_tables:
            item_frame = ctk.CTkFrame(self.tables_frame, width=100)
            item_frame.pack(pady=10, fill='x')
            button = ctk.CTkButton(item_frame, 
                                   width=300,
                                   height=80,
                                   text=table, 
                                   font=my_font,
                                   
                                   command=lambda data_list = db_tables[table]['Items'], 
                                   table_name = table: self.enter_list(data_list, table_name))
            button.pack()
            self.list_list.append(item_frame)
    

    def enter_list(self, data_list, table_name):
        ShowListFrame.table_list = data_list
        ShowListFrame.set_table(self.controller.frames['ShowListFrame'],table_name)
        ShowListFrame.create_item_list(app.frames['ShowListFrame'], data_list)
        self.controller.show_frame("ShowListFrame")

    def open_input_box(self):
        x = self.parent.winfo_rootx()
        y = self.parent.winfo_rooty()

        if self.input_box is None or not self.input_box.winfo_exists():
            self.input_box = AddTableWindow(self)
            self.input_box.geometry("+%d+%d" % (x + 25, y + 20))
        else:
            self.input_box.focus()

    def delete_list(self, table):
        db_tables.pop(table)
        delete_table(table)
        self.show_lists()


    
#---------------------------------------------------------------------------------------------------------------------------------------
class ShowListFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.input_box = None
        self.controller = controller
        self.parent = parent
        

        # external wrapping 
        add_quit_button_frame = ctk.CTkFrame(self, width=400)
        add_quit_button_frame.pack(fill='x')

        add_item_button = ctk.CTkButton(add_quit_button_frame, text='Add Item', width=30, command=self.open_input_box)
        add_item_button.pack(side='left', padx=10, pady=10)

        delete_list_button = ctk.CTkButton(add_quit_button_frame, text='Delete List', command=self.delete_list)
        delete_list_button.pack(side='left', padx=(58,0))

        quit_button = ctk.CTkButton(add_quit_button_frame, text='Quit', width=20, command=self.quit_app)
        quit_button.pack(side='left',padx=(90,10),pady=10)

        self.items_frame = ctk.CTkScrollableFrame(self, height=470, width=400, label_text='Grocery List', fg_color='#1e6b8a')
        self.items_frame.pack(anchor='n')

        # creates instance of item and adds to frame, to be replaced with add item function

        # Get Items from list and create widgets
        #self.create_item_list(test_data2)

        # delete items and back button
        delete_items_button = ctk.CTkButton(self, text='Delete Selected', command=lambda:self.delete_item(self.item_list))
        delete_items_button.pack(side='right', padx=10, pady=10)

        back_button = ctk.CTkButton(self, text='Go Back', command=lambda:controller.show_frame("AllListsFrame"))
        back_button.pack(side='left', padx=10, pady=10)
    
    def quit_app(self):
        cnx.commit()
        App.quit(self)

    def delete_list(self):
        AllListsFrame.delete_list(app.frames['AllListsFrame'], self.table)
        app.show_frame('AllListsFrame')

    def set_table(self, table):
        self.table = table
        self.items_frame.configure(label_text=table)

    def open_input_box(self):
        x = self.parent.winfo_rootx()
        y = self.parent.winfo_rooty()

        if self.input_box is None or not self.input_box.winfo_exists():
            self.input_box = AddItemWindow(self)
            self.input_box.geometry("+%d+%d" % (x + 50, y + 20))
        else:
            self.input_box.focus()

    def create_item_list(self, table_list):
        self.table_list = table_list
        if len(self.table_list) > 0: 
            self.destroy_items_in_items_frame()
            self.item_list = []
            for item in self.table_list:
                frame = ctk.CTkFrame(self.items_frame, width=300, fg_color='#0090c4', bg_color='black')
                frame.pack(side='top', anchor='n', pady=(0,20), fill='x')
                check_var = IntVar(frame, 0)
                checkbox = ctk.CTkCheckBox(frame, onvalue=1, offvalue=0, 
                                           variable=check_var, 
                                           text='', 
                                           checkbox_height=70, 
                                           checkbox_width=70,
                                           hover_color='#57d2ff', 
                                           checkmark_color='#cee5ed',
                                           bg_color='transparent')
                checkbox.pack(side='right', anchor='e', fill='both')
                frame.var = check_var

                for field in db_tables[self.table]['Fields']:
                    
                    field_label = ctk.CTkLabel(frame, 
                                               text=f"  {field.capitalize()}: {item[field]}", 
                                               font=my_font,
                                               text_color='#cee5ed',
                                               anchor='w', 
                                               bg_color='transparent')
                    field_label.pack(side='top', anchor='w', fill='x', expand='y')
                self.item_list.append(frame)
        else:
            for child in self.items_frame.winfo_children():
                child.destroy()
            label = ctk.CTkLabel(self.items_frame, text='empty')
            label.pack()



    def destroy_items_in_items_frame(self):
        deletion_tables = []
        for tables in db_tables:
            if db_tables[tables]['Items'] == []:
                deletion_tables.append(tables)
        #print(deletion_tables)
        
        #for table in deletion_tables:
            #db_tables.pop(table)

        #print(db_tables)

        for child in self.items_frame.winfo_children():
            child.destroy()

    def delete_item(self, item_list):
        destroy_index = []
    
        # is going backwards so when it gets to index 2 it doesnt see anything
        for index, item in enumerate(item_list):
            if item.var.get() == 1:
                destroy_index.append(index) 
                item.destroy()
    
        destroy_index.reverse()

        for index in destroy_index:
            delete_field = list(self.table_list[index].keys())[0]
            delete_value = self.table_list[index][delete_field]
            delete_entry(self.table, delete_field, delete_value)
            self.table_list.pop(index)
            item_list.pop(index)

        #if len(item_list) < 1:
            
            #AllListsFrame.show_lists(app.frames["AllListsFrame"])
            #self.controller.show_frame("AllListsFrame")

    def add_item(self, values, fields):
        self.destroy_items_in_items_frame()
        new_item = {}
        for field in fields:
            new_item[field] = values[fields.index(field)]    
        self.table_list.append(new_item)
        self.create_item_list(self.table_list)

#---------------------------------------------------------------------------------------------------------------------------------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry = ('400x600')

        # container that frames are displayed on
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill='y', expand='y', side='top')
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for F in (ShowListFrame, AllListsFrame):
            page_name = F.__name__
            if page_name == 'ShowListFrame':
                frame = F(self.container, self)
            else:
                frame = F(self.container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('AllListsFrame')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == '__main__':
    app = App()
    app.mainloop()
    
cnx.close()

# {'table':
#          [
#              [{'field': 'value', 'field2': 'value2'}], 
#              [{'field': 'value', 'field2': 'value2'}], 
#              [{'field': 'value', 'field2': 'value2'}]
#          ]
# }