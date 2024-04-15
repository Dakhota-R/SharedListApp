from tkinter import *

def create_button(root, text, row, column):
    button = Button(root, text=text)
    button.grid(row=row, column=column)