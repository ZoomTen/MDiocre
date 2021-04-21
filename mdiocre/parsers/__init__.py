def sub_func(match, v):
	'''
	Substitution function for use with `re.sub`.

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

	try:
		# variable = value
		return v.assign(statement)
	except SyntaxError as e:
		# if it isn't an assign statement,
		# get the variable name instead
		#print(e)
		return v.get(statement)

class BaseParser():
	'''
	This is the base class of which every MDiocre parser must
	be inheriting from. Even though this doesn't do much at the
	moment...
	'''
	def to_variables(self, text, v, ignore_content=False):
		'''
		Converts a string to a :class:`VariableManager`
		object. This should be reimplemented.
		
		Args:
		    text (string): The source file from which to
		        process and extract MDiocre commands from.
		    v (VariableManager): The object to which the
		        variables is processed and stored to.
		
		Returns:
		    A :class:`VariableManager` object.
		'''
		return v
