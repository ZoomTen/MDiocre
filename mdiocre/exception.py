#!/bin/python3
"""
Todo:
    Document these
"""
class InvalidVarName(Exception):
    def __init__(self, varname):
        self.varname = str(varname)
    def __str__(self):
        return "Invalid variable name: "+self.varname

class FileNotFound(Exception):
    def __init__(self, name):
        self.name = str(name)
    def __str__(self):
        return self.name+" not found!"

class QuoteMismatch(Exception):
    def __init__(self, string):
        self.string = str(string)
    def __str__(self):
        return "Mismatched quotes in string: "+self.string

class ConfigInvalid(Exception):
    pass
