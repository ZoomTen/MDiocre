import re
from . import BaseParser
import docutils.core
import docutils.nodes as nodes
import docutils.parsers.rst as rst

class RstParser(BaseParser):
	'''
	Instead of <!--:title = "Abc"-->
	it's :mdiocre:`title = "Abc"`
	'''
	
	# this doesn't match the roles matcher
	RE_COMMENTS = re.compile(r':mdiocre:`(.*?)`')
	
	def to_variables(self, markup, v, ignore_content=False):
		# custom mdiocre rst role
		def mdiocre_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
			command = text.strip()
			var_txt = ''
			try:
				# variable = value
				v.assign(command)
			except SyntaxError:
				# if it isn't an assign statement,
				# get the variable name instead
				var_txt = v.get(command)
			return [nodes.Text(var_txt)],[]
		
		rst.roles.register_local_role('mdiocre', mdiocre_role)
		
		# write html
		html = docutils.core.publish_parts(markup, writer_name='html')['html_body']
		
		# TODO: Write a custom HTML writer for this
		end_tag = '</div>'
		html = re.sub(r'<.+?>', '', html, count=1)
		html = html[:len(end_tag)*-1-1]
		html = html.strip()
		
		if not ignore_content:
			v.variables["content"] = html
		
		return v
