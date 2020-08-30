import sys

'''
Common tools used by MDiocre
'''

def declare(var_, type_):
	'''
	A substitute for static type-checking.
	
	Args:
	    var_ : The contents to check.
	    type_ (class) : A class type to check for
	'''
	if not type(type_) == type:
		raise TypeError('type_ to check must be a class')
	if not isinstance(var_, type_):
		raise TypeError('passed variable must be {} (is instead {})'.format('.'.join([type_.__module__, type_.__name__]), var_.__class__.__name__))
