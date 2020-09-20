'''
Common tools used by MDiocre. Internal use only
'''

def declare(var_, type_):
	'''
	A substitute for static type-checking.
	
	Args:
	    var_ : The contents to check.
	    type_ (class) : A class type to check for.
	'''
	if not type(type_) == type:
		raise TypeError('type_ to check must be a class')
	if not isinstance(var_, type_):
		raise TypeError('passed variable must be {} (is instead {})'.format('.'.join([type_.__module__, type_.__name__]), var_.__class__.__name__))
		

def remove_inner_outer_quotes(string):
	'''
	Remove any quotes around the text, with additional checking
	
	Args:
	    string (string): Text with quotes.
	
	Returns:
	    Text with removed quotes. Raises `SyntaxError` when there is no
	    matching quotes.
	'''
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
