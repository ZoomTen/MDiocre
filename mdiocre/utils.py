import re
import pypandoc as pd
import sys
import os
from .logger import Debug
from .exception import *

class Utils:
    """ Set up the utilities object.

    Parameters:
        logger (Debug): logger object to use.
            Defaults to a generated Debug object,
            with the extra notes set to `True`.
    Returns:
        Utils: A Utils object.
    """
    def __init__(self, logger=Debug(True)):
        #: mdiocre.logger.Debug: The logger used by the object.
        self.db = logger

    def check_exists(self, directory, name, strict=False, create=True, is_file=False, quiet=0):
        """ Check whether or not a file or directory exists

            Parameters:
                directory (str): File or directory to check
                name      (str): Name to show in the logger
                strict   (bool): Whether or not to throw an error
                    when the file doesn't exist. Defaults to `False`.
                create   (bool): Whether or not to create the file or
                    directory if it doesn't exist. Defaults to `True`.
                is_file  (bool): Whether or not the object to check
                    is really a file (not a directory). Defaults to `False`.
                quiet     (int): If 1, it will not display messages if
                    the file in question exists. If 2, it will not display
                    warnings as well. If 3, no output at all except exceptions.

            Returns:
                bool: Whether or not the file exists.

            Raises:
                FileNotFound: Raised when the ``strict`` parameter is set.
        """
        if not os.path.exists(directory):
            if strict:
                raise FileNotFound(directory)
                return
            else:
                if create:
                    if is_file:
                        open(directory, 'a').close()
                    else:
                        os.makedirs(directory)
                    if quiet < 2:
                        self.db.warning(name+" does not exist, creating.")
                    return True
                else:
                    if quiet < 2:
                        self.db.warning(name+" does not exist.")
                    return False
        else:
            if quiet < 1:
                self.db.log(name+" exists!")
            return True


    def convert_markdown_to_content(self, markdown, var_list={}, file_name=None):
        """ Tries to convert a Markdown-formatted string into HTML-formatted
            strings, with variable completion. Calls :py:func:`process_vars` twice
            to do so, one for setting the variables and the next for putting
            the variables on the string.

            Parameters:
                markdown   (str): Markdown-formatted string.
                var_list  (dict): A dictionary of variables to use. This
                    determines the scope of the page or site.
                file_name  (str): File name of the provided file, if any.

            Returns:
                str: The converted HTML string.
        """
        converted = self.process_vars(markdown, var_list=var_list, set_var=True, file_name=file_name)
        converted = self.process_vars(converted, var_list=var_list, file_name=file_name)
        html = pd.convert_text(converted, 'html', format="markdown")
        return html

    def process_vars(self, text, set_var=False, var_list={}, file_name=None):
        """ Process variables in html/markdown text

            Parameters:
                text       (str): A string; either Markdown or HTML.
                var_list  (dict): A dictionary of variables to use. This
                    determines the scope of the page or site.
                set_var   (bool): File name of the provided file, if any.
                file_name  (str): File name of the provided file, if any.

            Returns:
                str: The processed string.

            Raises:
                QuoteMismatch: When the variable setting has an uncompleted quote.

            Notes:
                The variables in this format, when used with mdiocre.Wizard,
                will be in the scope of the website.

                Using the variable system:

                1. Setting them.
                    ``<!--var_name=\"Text\"-->``
                        Store the string `Text` in `var_name`.
                    ``<!--var_name=\"Lorem ipsum\"-->``
                        Store the string `Lorem ipsum` in `var_name`.
                    ``<!--var_name=other_var-->``
                        Set `var_name` to the value of `other_var`.
                    ``<!--var_name=other_var, okay_var-->``
                        Set `var_name` to the value of `other_var` concatenated
                        with the value of `okay_var`
                    ``<!--var_name=other_var, - ,okay_var-->``
                        Set `var_name` to the value of `other_var` concatenated
                        with \" - \", then again to the value of `okay_var`,
                        resulting in the string \"`var_name` - `okay_var`\".

                2. Getting them / putting them in the document.
                    ``<!--var:var_name-->``
                        Replace the occurence of the comment with the
                        value of `var_name`.
                    ``<!--var:okay_var-->``
                        Replace the occurence of the comment with the
                        value of `okay_var`.

            Warning:
                There must be no spaces outside of concatenation and raw
                string assignments!

            Warning:
                If a variable is not defined, it will usually be emptied or
                just be an empty string.
        """
        def validate_quotes(string):
            has_quotes = False
            if (string[0] == "\"") or\
               (string[0] == "'"):
                has_quotes = True
                if string[0] != string[-1]:
                    raise QuoteMismatch(string)
            return has_quotes

        if type(file_name) is str:
            filename_warn = "In file: "+file_name+" - "
        else:
            filename_warn = ""

        # i can't figure out how to tokenize so oh
        if set_var:
            search = re.finditer(r'<!--([a-z\-_0-9]+)=(.+)-->', text)
        else:
            search = re.finditer(r'<!--var:([a-z\-_0-9]+)-->', text)
        starts, ends, matches = [], [], []
        cursor, final = 0, ""

        for entry in search:
            starts.append(entry.span()[0])
            ends.append(entry.span()[1])
            matches.append(entry.group(0)[4:-3]) if set_var\
       else matches.append(entry.group(0))

        for start, end, match in zip(starts, ends, matches):
            final += (text[cursor:start])

            if set_var:
                    var_name, value = match.split("=", 1)
                    var_name = var_name.strip()             # delete begin and end spaces
                    value = value.strip()
                    # Assign quoted strings
                    if validate_quotes(value):
                        var_list[var_name] = value[1:-1]
                    # Assign variables and operations
                    else:
                        if len(re.split(r',(?!.*")|,(?=\s*")',value)) > 1: # concat operation
                            o = ""
                            for x in re.split(r',(?!.*")|,(?=\s*")',value):
                                if validate_quotes(x.strip()):
                                    o += x.strip()[1:-1]
                                else:
                                    try:
                                        o += var_list[x.strip()]
                                    except KeyError:
                                        o += x  # assume string...
                                        self.db.warning(filename_warn+"Variable '"+x+"' does not exist, assuming it's a string...")
                            var_list[var_name] = o
                            self.db.log(filename_warn+"Assigned "+var_name+" to "+o+".")
                        else:                       # simple assign operation
                            try:
                                var_list[var_name] = var_list[value]
                            except KeyError:
                                self.db.warning(filename_warn+"Failed assigning "+var_name+" to "+value+", assuming string!")
                                var_list[var_name] = value.strip()
                            else:
                                self.db.log(filename_warn+"Assigned '"+var_name+"' to "+value+".")
            else:
                try:
                    var_name = match[8:-3]
                    final += var_list[var_name]
                except KeyError:
                    self.db.warning(filename_warn+"Undefined variable "+var_name+". Will display as an empty space!")	# change this to a log
                else:
                    #self.db.log("Contents of variable'"+var_name+"' in "+str(cursor))
                    pass
            # Everything else will just be ignored and rendered as regular HTML
            cursor = end
        final += (text[cursor:])
        return final
