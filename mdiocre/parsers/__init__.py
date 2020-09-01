def sub_func(match, v):
	'''
	Substitution function for use with `re.sub`.

	In MDiocre 3.0, this was used in nested form in :meth:`render`
	and :meth:`process`. Might be removed in 4.0.

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
		v.assign(statement)
		return ''
	except SyntaxError:
		# if it isn't an assign statement,
		# get the variable name instead
		return v.get(statement)

class BaseParser():
	def to_variables(self, text, v, ignore_content=False):
		return v
