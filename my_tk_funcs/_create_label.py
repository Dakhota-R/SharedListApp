from tkinter import * 

def create_label(root, text, row, column):
    label = Label(root, text=text)
    label.grid(row=row, column=column)
    return label