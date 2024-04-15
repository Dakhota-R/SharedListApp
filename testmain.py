import tkinter as tk

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(tk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text='nerd')
        label.pack(side='top', fill='both', expand=True)
        button = tk.Button(self, text='press me', command = lambda: print('send dudes'))
        button.pack(side='top', fill='both', expand=False)

    def show(self):
        self.lift()


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        p1 = Page1(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill='x', expand=False)
        container.pack(side='top', fill='both', expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        p1.show()

if __name__ == '__main__':
    root = tk.Tk()
    main = MainView(root)
    main.pack(side='top', fill='both', expand=True)
    root.wm_geometry("400x400")
    root.mainloop()

        