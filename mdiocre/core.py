from .utils import declare, remove_inner_outer_quotes
import logging
from .parsers import BaseParser, sub_func
import re
import os
import datetime
from importlib import import_module
from importlib.util import find_spec
'''
Core MDiocre conversion class
'''

logger = logging.getLogger('mdiocre.core')

RE_HTML_COMMENTS = re.compile(r'<!--:(.+?)-->')
RE_ASSIGNMENT = re.compile(r'.+=.+')
RE_KEYWORD = re.compile(r'.+:.+')
RE_ESCAPE = re.compile(r'(\\)(.{1})')

# This stupid complicated RE is necessary to enable reading commas in variables
RE_CONCAT = re.compile(
# Case 1
	r'('+	# Start capture group
		r'\"[^\"]*\"'+ # double-quoted strings
		r'|'+          # or
		r'\'[^\']*\''+ # single quoted strings
		r'|'+          # or
		r'\w+'+        # word
		r'|'+          # or
		r'\(.+\)'+     # function
	r')'+	# End capture group
	r',\s*'+       # Concat operator
	r'|'+          # Or
# Case 2
	r'('+	# Start capture group
		r'\"[^\"]*\"'+ # double-quoted strings
		r'|'+          # or
		r'\'[^\']*\''+ # single quoted strings
		r'|'           # or
		r'\w+'+        # word
		r'|'+          # or
		r'\(.+\)'+     # function
	r')'+	# End capture group
	r'$'	# EOL
)

class MDiocre():
	'''
	Main class to process source files and render HTML files.
	
	Args:
	    parser (Optional): a BaseParser-derived object. If both
	        `parser_name` and `parser` are defined, `parser` takes the
	        priority.
	    parser_name (str, Optional): The parser name. See :meth:`switch_parser`
	        for which ones are currently implemented.
	'''
	def __init__(self, parser=None, parser_name=None):
		if parser is None:
			if parser_name is None:
				# use markdown by default
				self.switch_parser("markdown")
			else:
				# type checking
				declare(parser_name, str)
				
				self.switch_parser(parser_name)
		else:
			if not issubclass(parser, BaseParser):
				raise ImportError("class {} must be a subclass of {}".format(parser.__name__, BaseParser.__name__)) from None
			self.parser = parser
	
	def switch_parser(self, name):
		'''
		Switch parsers by using an identifier or a class (not an instance!)
		derived from BaseParser.
		
		To implement a new parser, it must be a class with inherited from
		:class:`BaseParser`, Its name and file name must also
		match, e.g. a parser with the `html` identifier must
		be in `html.py` and have the class name of `HtmlParser`.
		
		Args:
		    name (string | :class:`BaseParser` ): Parser name or type.
		        If passed as a string, it will only take the following
		        values:
		        `markdown`, `html`, `rst`, `zim`, `gem`
		        
		        As a type, this function accepts it as long as it contains
		        a `to_variables`.
		
		.. warning::
		    Passing a `string` to `switch_parser` is deprecated as of
		    version 3.5. It will be removed in a future release.
		
		Returns:
		    None.
		'''
		
		if isinstance(name, type):
			if issubclass(name, BaseParser):
				self.parser = name()
				return
		
		# specifications for names
		# e.g. "markdown" -> MarkdownParser in parsers/markdown.py
		#   or "rst"      -> RstParser      in parsers/rst.py
		module_name = '.parsers.{}'.format(name.lower())
		class_name  = '{}Parser'.format(name.capitalize())
		# Switch parser
		
		if find_spec(module_name, 'mdiocre'):
			module = import_module(module_name, 'mdiocre')
		else:
			logger.error("{}: error occured: {}".format(name, e))
			raise Exception("Can't find any suitable modules")
		
		try:
			# internal-only
			module = import_module(module_name, 'mdiocre')
		except ModuleNotFoundError as e:
			logger.error("{}: error occured: {}".format(name, e))
			raise e
		else:
			module_class = getattr(module,class_name)
			if not issubclass(module_class, BaseParser):
				logger.error("{}: class {} must be a subclass of {}, not using.".format(name, class_name, BaseParser.__name__))
			else:
				self.parser = module_class()
	
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
	
	def parse_keyword(self, query):
		'''
		Currently called from :meth:`function`, this implements a few commands,
		or "keywords" that can be used to implement a little more modularity
		in one's templates/contents.
		
		Operands are separated by the colon `:`, on the left hand side is the
		keyword, on the right hand is the argument, assumed to be a string.
		
		The keyword is case-insensitive.
		
		They can be one of the following:
		    * **Include** : Essentially, it literally includes a file into the template or content. It can be used to set global variables, include common banners, etc. Its argument is a file RELATIVE TO THE WORKING DIRECTORY THE SCRIPT IS CALLED IN!
		          Example: ``Include: ../variables.html``
		    * **Using** : Load a Python script. You can use it to define a few functions which can be useful with the function call feature during assignment, for example to dynamically convert a few strings of text.
		          Example: ``Using: ../_functions.py``
		
		.. warning::
		    The `using` keyword executes raw Python code, so it may pose a
		    security risk! Use with caution, and double-check your source
		    files!
		
		Args:
		    query (string): Expects a string in the form of ``keyword : argument``.
		
		Returns:
		    None (or SyntaxError).
		'''
		# type checking
		declare(query, str)
		if not (re.match(RE_KEYWORD, query)):
			raise SyntaxError(f'<{query}> is neither a keyword nor an assign statement')
		
		keyword, value = query.split(':', 1)
		keyword = keyword.strip().lower()
		value = value.strip()
		
		# value quote
		if value[0] == '"' or value[0] == "'":
			value = remove_inner_outer_quotes(value)
		
		if keyword == "include":
			# include a raw file
			file_ = os.path.abspath(value)
			if os.path.isfile(file_):
				with open(file_, "r") as f_:
					# using MDiocre to render the include, calling this
					# in itself. epic
					m = MDiocre(parser_name='html')
					return m.render(f_.read(), self)
			return ''
		elif keyword == "using":
			file_ = os.path.abspath(value)
			# TODO: -----YIKES------------------------
			if os.path.isfile(file_):
				with open(file_, "r") as f_:
					exec(f_.read(), globals())
			# ----------------------------------------
			return ''
		else:
			raise SyntaxError(f'Supported keywords: include; using.')
		
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
		    * **Value assignment** : if the value is a variable name. This is assumed to be the default. Will assign
		      to an empty string if the variable is not found.
		          Example query: ``My Variable = Something else``
		    * **Function calls** : if a function is defined using the ``using``
		      keyword, it may be used for dynamic data conversion and processing. Surrounded by parentheses,
		      the word directly after it is the function name, followed by its arguments, surrounded by spaces.
		      Like regular Python, strings need to be in quotes. Arguments may be names of variables that are
		      already defined up to that point, they will be automatically substituted.
		          Example query: ``RSSDate = (toRFC822 PubDate)``
		
		..warning::
		    The function call feature executes raw Python code, so it may pose a
		    security risk! Use with caution, and double-check your source
		    files!
		
		Args:
		    query (string): Expects a string in the form of ``variable = value``.
		
		Returns:
		    None (or SyntaxError). If the variable is successfully assigned, its
                    value will be added to the object's ``variables`` dictionary.
		'''
		# type checking
		declare(query, str)
		if not (re.match(RE_ASSIGNMENT, query)):
			# if string matches " Something : Something else " do that instead
			return self.parse_keyword(query)
		
		# query expected to be "variable = value"
		ident, value = query.split('=', 1)
		ident = ident.strip()
		value = value.strip()
		
		# check valid identifier
		if ident in self.reserved_variable_names:
			raise SyntaxError(f'assignment <{query}>: variable name "{ident}" cannot be used!')
		
		concat_tokens = re.findall(RE_CONCAT, value)
		concat_tokens = list(map(lambda tok: tok[0] or tok[1], concat_tokens))
		concat_tokens = [x.strip() for x in concat_tokens]
		
		# start with a blank value
		value = ''
		for var in concat_tokens:
			# append each token according to the order
			# they appear
			if var[0] == '"' or var[0] == "'":
				# token is a string
				value += remove_inner_outer_quotes(var)
				
				# render all escaped characters
				def escape(match):
					return match.groups()[1]
				
				value = re.sub(RE_ESCAPE, escape, value)
			elif var[0] == "(":
				# token is a function call
				if var[-1] != ")":
					raise SyntaxError(f'Unmatched ( in assignment of {ident}')
				fn_tokens = [x.strip() for x in var[1:-1].split(" ")]
				
				for i in range(1, len(fn_tokens)):
					# transform arguments into variable contents
					if fn_tokens[i] in self.variables:
						escaped_var = self.variables[fn_tokens[i]].replace('"','\\"').replace("'","\\'")
						fn_tokens[i] = f"'{escaped_var}'"
				
				# TODO: -----YIKES------------------------
				loc = {}
				exec(f"__retval = {fn_tokens[0]}({','.join(fn_tokens[1:])})", globals(), loc)
				value += (loc['__retval'])
				# ----------------------------------------
			else:
				try:
					value += self.variables[var]
				except KeyError:
					value += ''
		
		self.variables[ident] = value
		
		return ''


