import sys

'''
Common tools used by MDiocre
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

def has_color():
	'''
	Borrowed from the `Django <https://github.com/django/django>`_ project.
	
	Returns:
	    True if the running system's terminal supports color, and False
	    otherwise.
	'''
	plat = sys.platform
	supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)

	is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
	return supported_platform and is_a_tty

class Logger():
	'''
	A color-enabled logger object.
	'''
	
	def print(self, *args, level=0, severity='info', **kwargs):
		'''
		Color and log enabled print function.
		
		Args:
		    level (int) : How much to indent
		    severity (str): Severity of the log. These can be:
		    
		        * ``info`` : Default terminal color.
		        * ``serious`` : Red.
		        * ``warning`` : Yellow.
		
		Returns:
		     None.
		'''
		color_enable = has_color()
		if color_enable:
			if severity=='info':
				print('\033[0m', end='', **kwargs)
			elif severity=='serious':
				print('\033[31m', end='', **kwargs)
			elif severity=='warning':
				print('\033[33m', end='', **kwargs)
		
		print(''.join(['    '*int(level), '...', *args]), end='', **kwargs)
		
		if color_enable:
			print('\033[0m', **kwargs)
		else:
			print('', **kwargs)

	def eprint(self, *args, level=0, severity='info', **kwargs):
		'''
		Convenience function to :meth:`print`, only that it outputs
		to stderr instead of stdout.
		
		Args: See :meth:`print`.
		
		Returns:
		    See :meth:`print`.
		'''
		return self.print(self, *args, level=level, severity=severity, file=sys.stderr, **kwargs)
