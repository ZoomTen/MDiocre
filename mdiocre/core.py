from .utils import declare
from markdown import Markdown
import re
import datetime

'''
Core MDiocre conversion class
'''

RE_MATH = re.compile(r'^\s*([-+]?)(\d+)(?:\s*([-+*\/])\s*((?:\s[-+])?\d+)\s*)+$')
RE_HTML_COMMENTS = re.compile(r'<!--:(.+?)-->')
RE_ASSIGNMENT = re.compile(r'.+=.+')
RE_CONCAT = re.compile(r'(.+?)[^\\],|(.+?)$')
RE_ESCAPE = re.compile(r'(\\)(.{1})')

class MDiocre():
	'''
	Main class to process Markdown source files and render HTML files.
	'''
	def __init__(self):
		pass
	
	def sub_func(self, match, v):
		'''
		Substitution function for use with `re.sub`.
		
		This is used in nested form in :meth:`render` and :meth:`process`.
		
		Args:
		    match (re.Match): object containing the string to be processed.
		    v (VariableManager): target variable manager object
		
		Returns:
		    If the string is in the form `variable = something`, it will
		    return a blank string, but stores the new value within `v.variables`.
		    Otherwise, it attempts to display the value of the variable
		    described, by running it through :meth:`VariableManager.get`.
		'''
		# type checking
		declare(match, re.Match)
		declare(v, VariableManager)
		
		statement = match.groups()[0]
		
		try:
			# variable = value
			v.assign(statement)
			return ''
		except SyntaxError:
			# if it isn't an assign statement,
			# get the variable name instead
			return v.get(statement)
	
	def render(self, template, variables):
		'''
		Renders a template with the specified variables.
		
		Due to the mechanism, template variables are separate from the
		page's variables, usually defined in the ``content`` variable.
		
		Args:
		    template (string): A string containing HTML comments.
		    variables (VariableManager): Variable object to use with
		        the template.
		
		Returns:
		    The processed string.
		'''
		# type checking
		declare(template, str)
		declare(variables, VariableManager)
		
		def render_sub_func(match):
			return self.sub_func(match, variables)
		
		# XXX: comment format necessary to parse MDiocre variables
		# template variables are processed separately since
		# the content is already proecessed
		converted = re.sub(RE_HTML_COMMENTS, render_sub_func, template)
		
		return converted
		
	
	def process(self, markdown, ignore_content=False):
		'''
		Process a Markdown string into a variable dictionary to use
		e.g. with :meth:`render`.
		
		Variables are processed by grabbing special HTML comments
		which start with ``<!--:`` More details about the conversion
		process can be found in :class:`VariableManager`.
		
		Args:
		    markdown (string): A string containing HTML comments.
		    ignore_content (bool, Optional): If True, it will not convert
		        the Markdown, rather it would only process the variables
		
		Returns:
		    A VariableManager object containing the processed variables,
		    that also contains the converted HTML under the ``content``
		    variable.
		'''
		# type checking
		declare(markdown, str)
		declare(ignore_content, bool)
		
		v = VariableManager()
		
		def conv_sub_func(match):
			return self.sub_func(match, v)
		
		# XXX: comment format necessary to parse MDiocre variables
		# process comments and search for special html comments
		markdown = re.sub(RE_HTML_COMMENTS, conv_sub_func, markdown)
		
		if not ignore_content:
			# XXX: main document converter
			md_parser = Markdown()
			converted = md_parser.convert(markdown)
			# content: a special variable containing the converted html
			v.variables["content"] = converted
		
		return v

def remove_inner_outer_quotes(string):
	if string[0] == '"':
		if not (string[-1] == '"'):
			raise SyntaxError('assignment <{}>: no matching end "'.format(string))
		string = string.strip('"')
	elif string[0] == "'":
		if not (string[-1] == "'"):
			raise SyntaxError("assignment <{}>: no matching end '".format(string))
		string = string.strip("'")
	elif string[-1] == '"':
		if not (string[0] == '"'):
			raise SyntaxError('assignment <{}>: no matching beginning "'.format(string))
		string = string.strip('"')
	elif string[-1] == "'":
		if not (string[0] == "'"):
			raise SyntaxError("assignment <{}>: no matching beginning '".format(string))
		string = string.strip("'")
	return string
	
class VariableManager():
	'''
	Variable manager.
	
	Variables are stored as a dictionary under `self.variables`. The identifiers
	can be any character except the = operator, which serves to separate the identifier
	and the value.
	
	.. warning::
	    There are a few reserved variables, which their names cannot be used, namely:
	        * **content** : The contents of a page that will be put into a template
	        * **mdiocre-gen-timestamp** : Timestamp of the generated content
	
	.. note::
	    The ``mdiocre-template`` variable is required when using the :class:`Wizard`.
	'''
	
	def __init__(self):
		self.variables = {}
		self.reserved_variable_names = ['content', 'mdiocre-gen-timestamp']
		
		# system variables
		self.variables['mdiocre-gen-timestamp'] = datetime.datetime.now().isoformat()
	
	def get(self, variable):
		'''
		Gets a variable from the variables list and returns its value.
		
		Args:
		    variable (string): Name of the variable.
		
		Returns:
		    String contents of the variable, or an empty string if the
		    variable is not found.
		'''
		# type checking
		declare(variable, str)
		
		variable = variable.strip()
		
		try:
			return str(self.variables[variable])
		except KeyError:
			return ''
	
	def assign(self, query):
		'''
		Assigns a variable to a value.
		
		The variable name has almost no limitations (especially not
		limitations usually posed by a programming language), but it is
		terminated by the `=` symbol.
		
		The value can be one of the following:
		    * **String** : if the value has quotes (single or double) around it.
		          Example query: ``My Variable = "Toast"``
		    * **Concatenation** : if two or more variable names are specified, with a comma separating each.
		          Example query: ``My Variable = Var 1, Var 2``
		    * **Math expression** : if the value is in the form of a simple math expression e.g. `1 * 2 + 3`
		          Example query: ``My Variable = 1 + 4 * 7 + 4 * 0``
		    * **Value assignment** : if the value is a variable name. This is assumed to be the default. Will assign
		      to an empty string if the variable is not found.
		          Example query: ``My Variable = Something else``
		
		Args:
		    query (string): Expects a string in the form of ``variable = value``.
		
		Returns:
		    None (or SyntaxError). If the variable is successfully assigned, its
                    value will be added to the object's ``variables`` dictionary.
		'''
		# type checking
		declare(query, str)
		if not (re.match(RE_ASSIGNMENT, query)):
			raise SyntaxError('<{}> is not an assign statement'.format(query))
		
		# query expected to be "variable = value"
		ident, value = query.split('=', 1)
		ident = ident.strip()
		value = value.strip()
		
		# check valid identifier
		if ident in self.reserved_variable_names:
			raise SyntaxError('assignment <{}>: variable name "{}" cannot be used!'.format(query, ident))
		
		# do some maths
		if re.match(RE_MATH, value):
			# we don't yet accept parentheses
			p = re.match(RE_MATH, value)
			
			# yiiiiiiiiiiiiikes
			value = str(eval(value))
		# if not, assume concat
		else:
			concat_vars = []
			
			concat_tokens = re.findall(RE_CONCAT, value)
			
			# add each token to concat_vars
			# you get pairs like ('', '', 'lol')
			# due to the regex
			for token in concat_tokens:
				for el in token:
					if el != '':
						# remove whitespace from each token
						el = el.strip()
						concat_vars.append(el)
			
			# start with a blank value
			value = ''
			for var in concat_vars:
				# append each token according to the order
				# they appear
				if var[0] == '"' or var[0] == "'":
					value += remove_inner_outer_quotes(var)
					
					# render all escaped characters
					def escape(match):
						return match.groups()[1]
					
					value = re.sub(RE_ESCAPE, escape, value)
				else:
					try:
						value += self.variables[var]
					except KeyError:
						value += ''
		
		self.variables[ident] = value


