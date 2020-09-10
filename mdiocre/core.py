from .utils import declare, remove_inner_outer_quotes, Logger
from .parsers import BaseParser, sub_func
import re
import datetime
from importlib import import_module
'''
Core MDiocre conversion class
'''

RE_HTML_COMMENTS = re.compile(r'<!--:(.+?)-->')
RE_MATH = re.compile(r'^\s*([-+]?)(\d+)(?:\s*([-+*\/])\s*((?:\s[-+])?\d+)\s*)+$')
RE_ASSIGNMENT = re.compile(r'.+=.+')
RE_CONCAT = re.compile(r'(.+?)[^\\],|(.+?)$')
RE_ESCAPE = re.compile(r'(\\)(.{1})')

class MDiocre():
	'''
	Main class to process Markdown source files and render HTML files.
	
	Args:
	    parser (Optional): a BaseParser-derived object. If both
	        `parser_name` and `parser` are defined, `parser` takes the
	        priority.
	    parser_name (Optional): The parser name. See :meth:`switch_parser`
	        for which ones are currently implemented.
	'''
	def __init__(self, parser=None, parser_name=None):
		if parser is None:
			if parser_name is None:
				# use markdown by default
				self.switch_parser("markdown")
			else:
				self.switch_parser(parser_name)
		else:
			if not issubclass(parser, BaseParser):
				raise ImportError("class {} must be a subclass of {}".format(parser.__name__, BaseParser.__name__)) from None
			self.parser = parser
	
	def switch_parser(self, name):
		'''
		Switch parsers by using an identifier. To implement a
		new parser, it must be a class with inherited from
		:class:`BaseParser`, Its name and file name must also
		match, e.g. a parser with the `html` identifier must
		be in `html.py` and have the class name of `HtmlParser`.
		
		Args:
		    name (string): Parser name. Currently implemented:
		        `markdown`, `html`, `rst`
		
		Returns:
		    None.
		'''
		# Postulations for names
		module_name = '.parsers.{}'.format(name.lower())
		class_name  = '{}Parser'.format(name.capitalize())
		# Switch parser
		try:
			module = import_module(module_name, 'mdiocre')
		except Exception as e:
			Logger().eprint("{}: error occured: {}".format(name, e), level=0, severity='serious')
		else:
			module_class = getattr(module,class_name)
			if not issubclass(module_class, BaseParser):
				Logger().eprint("{}: class {} must be a subclass of {}, not using.".format(name, class_name, BaseParser.__name__), level=0, severity='serious')
			else:
				self.parser = module_class()
	
	def sub_func(self, match, v):
		'''
		Moved to :meth:`mdiocre.parsers.sub_func`. Will remove in
		MDiocre 3.2.
		'''
		return sub_func(match, v)
	
	def render(self, template, variables):
		'''
		Renders a template with the specified variables.
		
		Due to the mechanism, template variables are separate from the
		page's variables. The converted page is defined in the
		``content`` variable, and can be used by templates to render
		the documents.
		
		Args:
		    template (string): A string containing formatted comments.
		    variables (VariableManager): Variable object to use with
		        the template.
		
		Returns:
		    The processed string.
		'''
		# type checking
		declare(template, str)
		declare(variables, VariableManager)
		
		def render_sub_func(match):
			return sub_func(match, variables)
		
		# TODO: implement the same parser as process
		# template variables are processed separately since
		# the content is already proecessed
		converted = re.sub(RE_HTML_COMMENTS, render_sub_func, template)
		
		return converted
		
	def process(self, string, ignore_content=False):
		'''
		Process a string into a variable dictionary to use
		e.g. with :meth:`render`.
		
		The string is processed according to
		a parser that converts it to HTML and extracts any MDiocre
		"commands". For Markdown and HTML, these are stuff that is
		prefixed with `<!--:`, for RST, it's `:mdiocre:`.
		
		More details about the conversion process can be found in
		:class:`VariableManager`.
		
		As of 3.1, this is really a wrapper for all the parsers.
		
		Args:
		    string (string): A string containing MDiocre commands.
		    ignore_content (bool, Optional): If True, it will not convert
		        the string to the `content` variable.
		
		Returns:
		    A VariableManager object containing the processed variables,
		    that also contains the converted HTML under the ``content``
		    variable, if `ignore_content` is `False`.
		'''
		# type checking
		declare(string, str)
		declare(ignore_content, bool)
		
		v = VariableManager()
		
		return self.parser.to_variables(string, v, ignore_content=ignore_content)
	
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
			print('assignment <{}>: variable name "{}" cannot be used!'.format(query, ident))
		
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


