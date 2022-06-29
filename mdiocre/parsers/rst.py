import re
from . import BaseParser
import docutils.core
import docutils.nodes as nodes
import docutils.parsers.rst as rst
from docutils.writers import html4css1

class CustomHTMLTranslator(html4css1.HTMLTranslator):
	def should_be_compact_paragraph(self, node):
		# check for empty nodes
		num_empty = 0
		for i in list(node):
			text = i.astext()
			if re.match(r'\n$', text):
				num_empty += 1
			elif re.match(r'\s*$', text):
				num_empty += 1
		empty = (num_empty == len(list(node)))
		if empty:
			return True
		if(isinstance(node.parent, nodes.block_quote)):
			return False
		return html4css1.HTMLTranslator.should_be_compact_paragraph(self, node)
	
	def visit_paragraph(self, node):
		if self.should_be_compact_paragraph(node):
			self.context.append('')
		else:
			self.body.append(self.starttag(node, 'p', ''))
			self.context.append('</p>\n')
	
	def depart_paragraph(self, node):
		self.body.append(self.context.pop())

	def visit_section(self, node):
		self.section_level += 1

	def depart_section(self, node):
		self.section_level -= 1

	def visit_container(self, node):
		# lightweight divs
		self.body.append(self.starttag(node, 'div'))

class CustomHTMLWriter(html4css1.Writer):
	def __init__(self):
		html4css1.Writer.__init__(self)
		self.translator_class = CustomHTMLTranslator

class RstParser(BaseParser):
	'''
	In ReStructuredText, MDiocre commands are its' own
	RST role, "mdiocre".
	'''
	
	FILETYPES = ["rst"]
	
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
		html = docutils.core.publish_parts(markup, writer=CustomHTMLWriter())['html_body']
		
		# TODO: Write a custom HTML writer for this
		end_tag = '</div>'
		html = re.sub(r'<.+?>', '', html, count=1)
		html = html[:len(end_tag)*-1-1]
		html = html.strip()
		
		if not ignore_content:
			v.variables["content"] = html
		
		return v
