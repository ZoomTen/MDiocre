import os
import colorama
from colorama import Fore, Style
import logging as log

class Debug:
    """
    Todo:
        Document this
    """
    def __init__(self,debug=False,file_name=None):
        self.debug = debug
        colorama.init()
        from imp import reload
        reload(log)
        if type(file_name) is str:
            log.basicConfig(filename=file_name,
                                    level=log.DEBUG,
                                    format='%(asctime)s %(message)s',
                                    datefmt='%m/%d/%Y %I:%M:%S')
        else:
            log.basicConfig(level=99999,
                                    format='%(message)s')
        self.logger = log
        self.logger.info("\n\nStart new log")

    def header(self,header, istitle):
        # Prints process name, 0th level. Prints:
        # === PERFORMING Doing action ===
        # if istitle=True, or prints:
        # Doing action
        # otherwise.
        # I: str, bool
        # O: -
        if istitle:
            #print("\n=== PERFORMING %s ===" % header)
            print(Fore.GREEN+"\n=== PERFORMING "+header+" ==="+Style.RESET_ALL)
            self.logger.info("=== PERFORMING %s ===", header)
        else:
            #print(header)
            self.logger.info(header)
            print(Fore.GREEN+header+Style.RESET_ALL)

    def name(self,string):
        # Prints process name, 1st level. Prints:
        # ... Doing action
        # Printed to terminal if o.debug is True.
        # I: str
        # O: -
        s = "... "+string
        self.logger.info(s)
        if self.debug:
            print(s)
    def log(self,string):
        # Prints process name, 2nd level. Prints:
        #         Doing action
        # Printed to terminal if o.debug is True.
        # I: str
        # O: -
        s = "        "+string
        self.logger.info(s)
        if self.debug:
            #print(s)
            print(Fore.CYAN+s+Style.RESET_ALL)

    def error(self,string):
        # Prints error string onto the terminal.
        # I: str
        # O: -
        s = "  ERROR: "+string+"\n"
        self.logger.error(s)
        print(Fore.RED+s+Style.RESET_ALL)

    def warning(self,string):
        # Prints error string onto the terminal.
        # I: str
        # O: -
        s = "  WARNING: "+string
        self.logger.warning(s)
        #print(s)
        print(Fore.YELLOW+s+Style.RESET_ALL)
