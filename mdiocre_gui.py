import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from ttkthemes import ThemedTk

import webbrowser

class AppMenu(tk.Frame):
    def __init__(self, root):
        # setup menu bar
        frame = tk.Frame(root)
        menu_bar = tk.Menu(frame)
        
        # setup file menu
        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label='Exit', command=root.destroy)
        
        # setup help menu
        help_menu = tk.Menu(menu_bar, tearoff=False)
        help_menu.add_command(label='About', command=self.about_popup)
        help_menu.add_command(label='File a bug', command=self.open_issues_page)

        # add menus
        menu_bar.add_cascade(label='File', menu=file_menu)
        menu_bar.add_cascade(label='Help', menu=help_menu)
        
        # apply menubar
        root.config(menu=menu_bar)

    def about_popup(self):
        showinfo('MDiocre-GUI', 'MDiocre GUI v1.0 (MD3.1)\n(c) 2020 Zumi')

    def open_issues_page(self):
        pass

class Main(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.create_title()
        self.create_pages()
        self.build_page()

    def build_page(self):
        root = self.build_frame
        text = tk.Text(root, padx=10, pady=10)
        text.pack()

    def create_title(self):
        title = tk.Label(self.root, text='MDiocre-GUI')
        title.configure(font=('sans',24,'bold'))
        title.pack(padx=10, pady=10)

    def create_pages(self):
        # create notebook widget
        tabs = ttk.Notebook(self.root)

        # create pages
        self.build_frame = ttk.Frame(tabs)
        self.process_frame = ttk.Frame(tabs)
        self.str_frame = ttk.Frame(tabs)

        # assign each to a tab
        tabs.add(self.build_frame, text=' Build a directory ')
        tabs.add(self.process_frame, text=' Process a file ')
        tabs.add(self.str_frame, text=' Process a string ')

        # add the tab + pages
        tabs.pack(expand=True, fill='both', padx=10, pady=10)

if __name__ == "__main__":
    # setup window
    window = ThemedTk(theme='elegance')
    #style = ttk.Style()

    window.title('MDiocre-GUI')
    
    # load up widgets
    AppMenu(window)
    Main(window)
    
    # apply style
    #style.theme_use('clam')

    # run
    window.mainloop()
