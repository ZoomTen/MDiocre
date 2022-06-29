import re
from . import BaseParser, sub_func

class HtmlParser(BaseParser):
	'''
	In HTML, MDiocre commands are HTML comments prefixed
	with ``<!--:``.
	'''
	
	FILETYPES = ["html", "htm"]

	RE_COMMENTS = re.compile(r'<!--:(.+?)-->')
	
	def to_variables(self, html, v, ignore_content=False):
		def trf_sub_func(match):
			return sub_func(match, v)
		
		html = re.sub(self.RE_COMMENTS, trf_sub_func, html)
		
		if not ignore_content:
			v.variables["content"] = html
			
		return v
