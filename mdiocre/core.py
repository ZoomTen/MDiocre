from markdown import Markdown
import re
import datetime

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
		statement = match.groups()[0]
		if(re.match(r'.+=.+', statement)):
			v.assign(statement)
			return ''
		else:
			return v.get(statement)
	
	def render(self, template, variables):
		'''
		Renders a template with the specified variables.
		
		Due to the mechanism, template variables are separate from the
		page's variables, usually defined in "content".
		
		Args:
		    template (string): An HTML string.
		    variables (VariableManager): Variable object to use with
		        the template.
		
		Returns:
		    String containing the processed HTML.
		'''
		def render_sub_func(match):
			return self.sub_func(match, variables)
		
		# template variables are processed separately since
		# the content is already proecessed
		converted = re.sub(r'<!--:(.+)-->', render_sub_func, template)
		
		return converted
		
	
	def process(self, markdown):
		'''
		Process a Markdown string into a variable dictionary to use
		e.g. with :meth:`render`.
		
		Variables are processed by grabbing special HTML comments
		which start with ``<!--:`` More details about the conversion
		process can be found in :class:`VariableManager`.
		
		Args:
		    markdown (string): A Markdown string.
		
		Returns:
		    A VariableManager object containing the processed variables,
		    that also contains the converted HTML under the "content"
		    variable.
		'''
		md_parser = Markdown()
		
		v = VariableManager()
		
		def conv_sub_func(match):
			return self.sub_func(match, v)
		
		# process comments and search for special html comments
		markdown = re.sub(r'<!--:(.+)-->', conv_sub_func, markdown)
		
		converted = md_parser.convert(markdown)
		
		# content: a special variable containing the converted html
		v.variables["content"] = converted
		
		return v

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
		try:
			return str(self.variables[variable])
		except KeyError:
			return ''
	
	def assign(self, query):
		'''
		Assigns a variable to a value.
		
		The value can be one of the following:
		    * **String** : if the value has quotes (single or double) around it.
		    * **Concatenation** : if two or more variable names are specified, with a comma separating each.
		    * **Math expression** : if the value is in the form of a simple math expression e.g. `1 * 2 + 3`
		    * **Value assignment** : if the value is a variable name. This is assumed to be the default. Will assign
		      to an empty string if the variable is not found.
		
		Args:
		    query (string): Expects a form of `variable = value`.
		
		Returns:
		    Depends on the assigned value.
		'''
		# query expected to be "variable = value"
		ident, value = query.split('=')
		ident = ident.strip()
		value = value.strip()
		
		RE_MATH = re.compile(r'^\s*([-+]?)(\d+)(?:\s*([-+*\/])\s*((?:\s[-+])?\d+)\s*)+$')
		
		# check valid identifier
		if ident in self.reserved_variable_names:
			raise SyntaxError('assignment <{}>: variable name "{}" cannot be used!'.format(query, ident))
		# check for string type, so check outer quotes
		if value[0] == '"':
			if not (value[-1] == '"'):
				raise SyntaxError('assignment <{}>: no matching end "'.format(query))
			value = value.strip('"')
		elif value[0] == "'":
			if not (value[-1] == "'"):
				raise SyntaxError("assignment <{}>: no matching end '".format(query))
			value = value.strip("'")
		elif value[-1] == '"':
			if not (value[0] == '"'):
				raise SyntaxError('assignment <{}>: no matching beginning "'.format(query))
			value = value.strip('"')
		elif value[-1] == "'":
			if not (value[0] == "'"):
				raise SyntaxError("assignment <{}>: no matching beginning '".format(query))
			value = value.strip("'")
		# if not, check for concatenation
		elif len(value.split(',')) > 1:
			concat_vars = [var.strip() for var in value.split(',')]
			try:
				value = ''.join([self.variables[var] for var in concat_vars])
			except KeyError:
				value = ''
		# if not, do some maths
		elif re.match(RE_MATH, value):
			# we don't yet accept parentheses
			p = re.match(RE_MATH, value)
			
			# yiiiiiiiiiiiiikes
			value = str(eval(value))
		# if not, assume it's a whole variable
		else:
			try:
				value = self.variables[value]
			except KeyError:
				value = ''
		
		self.variables[ident] = value


