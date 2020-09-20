#!/usr/bin/python

GUI_VERSION = '1.0.0.dev1'

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror

from ttkthemes import ThemedTk

import webbrowser

from mdiocre.wizard import Wizard
from mdiocre.__meta__ import __version__ as MD_VERSION

import contextlib
from io import StringIO

import sys
import os

log_txt = '''MDiocre GUI {} ready.

Supported extensions: *.md, *.html, *.htm, *.rst.
Info: Files that will be processed by MDiocre must
      have the 'mdiocre-template' set.
Press 'Process' to start.
'''.format(GUI_VERSION)

def append_line(text):
    global log_txt
    log_txt += '\n{}'.format(text)

def set_log(text):
    global log_txt
    log_txt = text

class AppMenu(ttk.Frame):
    def __init__(self, root):
        # setup menu bar
        frame = ttk.Frame(root)
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
        
        #menu_bar.configure(bg='#FCB64F')
        
        # apply menubar
        root.config(menu=menu_bar)

    def about_popup(self):
        showinfo('MDiocre-GUI', 'MDiocre GUI {} (MD: {})\n(c) 2020 Zumi'.format(GUI_VERSION, MD_VERSION))

    def open_issues_page(self):
        pass

class Main(ttk.Frame):
    def __init__(self, root):
        self.root = root
        self.tab_actions = {}
        self.create_title()
        self.create_pages()
        self.build_page()
        self.process_page()
        self.make_buttons()

    def make_buttons(self):
        root = self.root

        def process_button():
            selected_tab = self.tabs.index(self.tabs.select())
            action = self.tab_actions[selected_tab]
            print('tab {}, action {}'.format(selected_tab, action.__name__))
            action()

        tool_frm = ttk.Frame(root)
        #cancel_btn = ttk.Button(tool_frm)
        #cancel_btn.config(text='Cancel')
        #cancel_btn.pack(side='right', padx='10')
        process_btn = ttk.Button(tool_frm)
        process_btn.config(text='Process')
        process_btn.configure(command=process_button)
        process_btn.pack(side='right', padx='10')
        tool_frm.pack(side='bottom', fill=tk.X)
    
    def set_tab_action(self, tab_number, func):
        self.tab_actions[tab_number] = func
    
    def update_log(self):
        self.message_2.config(state='normal')
        self.message_2.delete(1.0, tk.END)
        self.message_2.insert(0.0, log_txt)
        self.message_2.config(state='disabled')
        self.message_2.see("end")
        #self.message_2.after(10, self.update_log)

    def build_page(self):
        root = self.build_frame
        
        # source directory
        def set_source():
            directory = filedialog.askdirectory()
            source_dir_etr.delete('0', 'end')
            source_dir_etr.insert('0', directory)
        
        def set_build():
            directory = filedialog.askdirectory()
            build_dir_etr.delete('0', 'end')
            build_dir_etr.insert('0', directory)
        
        def do_build():
            src = source_dir_etr.get()
            dst = build_dir_etr.get()

            if not os.path.exists(src):
                showerror('Source does not exist!', "Source path: {}\n doesn't exist".format(src))
            else:
                c = StringIO()
                w = Wizard()
                with contextlib.redirect_stdout(c):
                    # TODO: This is locking!
                    w.generate_from_directory({'source_dir':src,'build_dir':dst})
                c.seek(0)
                append_line(c.read())
                self.update_log()

        source_dir_frm = ttk.Frame(root)
        source_dir_txt = ttk.Label(source_dir_frm)
        source_dir_txt.config(font=('sans',10,'bold'), text='Source')
        source_dir_txt.pack(side='left', padx='5', pady='5')
        source_dir_etr = ttk.Entry(source_dir_frm)
        source_dir_etr.delete('0', 'end')
        source_dir_etr.insert('0', '')
        source_dir_etr.pack(side='left', ipadx='0', ipady='5', padx='5', pady='5', fill=tk.X, expand=1)
        source_dir_btn = ttk.Button(source_dir_frm)
        source_dir_btn.config(text='Open directory')
        source_dir_btn.configure(command=set_source)
        source_dir_btn.pack(side='left', padx='5', pady='5')
        source_dir_frm.pack(side='top', padx='10', pady='10', fill=tk.X)
        
        # build directory
        build_dir_frm = ttk.Frame(root)
        build_dir_txt = ttk.Label(build_dir_frm)
        build_dir_txt.config(font=('sans',10,'bold'), text='Destination')
        build_dir_txt.pack(side='left', padx='5', pady='5')
        build_dir_etr = ttk.Entry(build_dir_frm)
        build_dir_etr.delete('0', 'end')
        build_dir_etr.insert('0', '')
        build_dir_etr.pack(side='left', ipadx='0', ipady='5', padx='5', pady='5', fill=tk.X, expand=1)
        build_dir_btn = ttk.Button(build_dir_frm)
        build_dir_btn.config(text='Open directory')
        build_dir_btn.configure(command=set_build)
        build_dir_btn.pack(side='left', padx='5', pady='5')
        build_dir_frm.pack(side='top', padx='10', pady='10', fill=tk.X)
        
        # log
        self.message_2 = tk.Text(root,height=0)
        self.message_2.config(font='{monospace} 10 {}')
        #self.message_2.configure(bg='#A0541A', fg='#fff')
        self.message_2.insert(0.0, log_txt)
        self.message_2.config(state='disabled')
        self.message_2.pack(side='top', ipadx='5', ipady='5', padx='5', pady='5', fill=tk.BOTH, expand=1)
        #self.message_2.after(10, self.update_log)

        # set the process function
        self.set_tab_action(0, do_build)
    
    def process_page(self):
        pass
    
    def create_title(self):
        title = ttk.Label(self.root, text='MDiocre-GUI')
        title.configure(font=('sans',24,'bold'))
        title.pack(padx=10, pady=10)

    def create_pages(self):
        # create notebook widget
        self.tabs = ttk.Notebook(self.root)

        # create pages
        self.build_frame = ttk.Frame(self.tabs)
        #self.process_frame = ttk.Frame(self.tabs)
        #self.str_frame = ttk.Frame(self.tabs)

        # assign each to a tab
        self.tabs.add(self.build_frame, text=' Build a directory ')
        #self.tabs.add(self.process_frame, text=' Process a file ')
        #self.tabs.add(self.str_frame, text=' Process a string ')

        # add the tab + pages
        self.tabs.pack(expand=True, fill='both', padx=10, pady=10)

def gui():
    # setup window
    #window = ThemedTk(theme='elegance')
    window = tk.Tk()
    style = ttk.Style()

    window.title('MDiocre-GUI')
    #window.configure(bg='#FCB64F')
    
    main_frame = ttk.Frame(window)
    
    # load up widgets
    AppMenu(window)
    Main(window)
    
    # apply style
    style.theme_use('clam')

    # run
    window.mainloop()
   
if __name__ == "__main__":
    gui()
