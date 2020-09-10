#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo

from ttkthemes import ThemedTk

import webbrowser

log_txt = '''MDiocre GUI 1.0 ready.

Supported extensions: *.md, *.html, *.htm, *.rst.
Info: Files that will be processed by MDiocre must
      have the 'mdiocre-template' set.
Press 'Process' to start.
'''

class Runner(object):  
    def append_line(self, text):
            global log_txt
            log_txt += '\n{}'.format(text)

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
        
        menu_bar.configure(bg='#FCB64F')
        
        # apply menubar
        root.config(menu=menu_bar)

    def about_popup(self):
        showinfo('MDiocre-GUI', 'MDiocre GUI v1.0 (MD3.1)\n(c) 2020 Zumi')

    def open_issues_page(self):
        pass

class Main(ttk.Frame):
    def __init__(self, root):
        self.root = root
        self.create_title()
        self.create_pages()
        self.build_page()
        self.process_page()
        self.make_buttons()

    def make_buttons(self):
        root = self.root
        tool_frm = ttk.Frame(root)
        cancel_btn = ttk.Button(tool_frm)
        cancel_btn.config(text='Cancel')
        cancel_btn.pack(side='right', padx='10')
        process_btn = ttk.Button(tool_frm)
        process_btn.config(text='Process')
        process_btn.pack(side='right', padx='10')
        tool_frm.pack(side='bottom', fill=tk.X)
        
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
            # update the log window
            #message_2.config(state='normal')
            #message_2.delete(1.0, tk.END)
            #message_2.insert(0.0, log_txt)
            #message_2.config(state='disabled')

        source_dir_frm = ttk.Frame(root)
        source_dir_txt = ttk.Label(source_dir_frm)
        source_dir_txt.config(font=('sans',10,'bold'), text='Source')
        source_dir_txt.pack(side='left', padx='5', pady='5')
        source_dir_etr = ttk.Entry(source_dir_frm)
        source_dir_etr.delete('0', 'end')
        source_dir_etr.insert('0', 'File')
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
        build_dir_etr.insert('0', 'File')
        build_dir_etr.pack(side='left', ipadx='0', ipady='5', padx='5', pady='5', fill=tk.X, expand=1)
        build_dir_btn = ttk.Button(build_dir_frm)
        build_dir_btn.config(text='Open directory')
        build_dir_btn.configure(command=set_build)
        build_dir_btn.pack(side='left', padx='5', pady='5')
        build_dir_frm.pack(side='top', padx='10', pady='10', fill=tk.X)
        
        # log
        message_2 = tk.Text(root,height=0)
        message_2.config(font='{monospace} 10 {}')
        message_2.configure(bg='#A0541A', fg='#fff')
        message_2.insert(0.0, log_txt)
        message_2.config(state='disabled')
        message_2.pack(side='top', ipadx='5', ipady='5', padx='5', pady='5', fill=tk.BOTH, expand=1)
    
    def process_page(self):
        pass
    
    def create_title(self):
        title = ttk.Label(self.root, text='MDiocre-GUI')
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
    window = ThemedTk(theme='kroc')
    
    #style = ttk.Style()

    window.title('MDiocre-GUI')
    window.configure(bg='#FCB64F')
    
    main_frame = ttk.Frame(window)
    
    # load up widgets
    AppMenu(window)
    Main(window)
    
    # apply style
    #style.theme_use('clam')

    # run
    window.mainloop()
