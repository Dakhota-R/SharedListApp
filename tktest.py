from tkinter import *
import customtkinter

test_data = [['pineapple', '5$', '5'], ['tube', '3$', '2'], ['donut', '23$', '1'], ['donut', '23$', '1'], ['donut', '23$', '1'], ['donut', '23$', '1'], ['donut', '23$', '1'], ['donut', '23$', '1'], ['donut', '23$', '1'], ['donut', '23$', '1'], ['donut', '23$', '1'], ['donut', '23$', '1']]

class Item(customtkinter.CTkFrame):

    def __init__(self, name, price, quantity, ids):
        self.name = name
        self.price = price
        self.quantity = quantity
        
        self.selected = StringVar()
        self.id = ids

    def checkbox_event(self):
        pass
        #print(self.selected.get())
        #print(self.id)

    def create_item(self, item_frame):
        item = customtkinter.CTkFrame(item_frame)
        item.pack(anchor='w', pady = 5)

        # Checkbox and item name
        cni_frame = customtkinter.CTkFrame(item)
        cni_frame.pack(anchor='w')
        item_checkbox = customtkinter.CTkCheckBox(cni_frame, text='', width=3, command=self.checkbox_event, variable=self.selected, onvalue='on', offvalue='off')
        item_checkbox.grid(row=0)
        item_name = customtkinter.CTkLabel(cni_frame, text=self.name, font=('arial', 40), width=12, anchor='w')
        item_name.grid(row=0, column=1)

        # Item price and quantity
        pnq_frame = customtkinter.CTkFrame(item)
        pnq_frame.pack(anchor='w', padx=(50,0), pady=(10,0))
        item_price = customtkinter.CTkLabel(pnq_frame, text="Price: " + self.price, font=('arial', 25), width=15,anchor='w')
        item_price.grid(row=0)
        item_quantity = customtkinter.CTkLabel(pnq_frame, text="Amount: " + self.quantity, font=('arial', 25), width=11, anchor='w')
        item_quantity.grid(row=1)


class Frame1(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        wrapper = customtkinter.CTkFrame(root, width=400, height=600)
        wrapper.pack(fill='y', expand='y')

        add_quit_button_frame = customtkinter.CTkFrame(wrapper)
        add_quit_button_frame.pack()

        add_item_button = customtkinter.CTkButton(add_quit_button_frame, text='Add Item', width=30)
        add_item_button.pack(side='left',expand='y',padx=(0,100))

        quit_button = customtkinter.CTkButton(add_quit_button_frame, text='Quit', width=20, command=root.quit)
        quit_button.pack(side='right', anchor='e', fill='y')

        items_frame = customtkinter.CTkScrollableFrame(wrapper, height=470, width=400, label_text='Grocery List')
        items_frame.pack(anchor='n')

        self.current_items = []
        for index, item in enumerate(test_data):
            itemobj = Item(item[0], item[1], item[2], index)     
            itemobj.create_item(items_frame)
        #   self.current_items.append(itemobj)


        back_button = customtkinter.CTkButton(wrapper, text='Go Back')
        back_button.pack(side='left',fill='y', expand='y')

        delete_button = customtkinter.CTkButton(wrapper, text='Delete Selected')
        delete_button.pack(side='right', fill='y', expand='y')

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry=('400x600')
        self.title = ('List App')

        self.frame = Frame1(self)

# Loop
if __name__ == '__main__':
    app = App()
    app.mainloop()
