# fallback

import re
from . import BaseParser, sub_func
from markdown import Markdown
from mdx_gfm import GithubFlavoredMarkdownExtension

class MarkdownParser(BaseParser):
	'''
	In Markdown, MDiocre commands are HTML comments prefixed
	with ``<!--:``.
	'''
	
	FILETYPES = ["md"]
	
	RE_COMMENTS = re.compile(r'<!--:(.+?)-->')
	
	def to_variables(self, markdown, v, ignore_content=False):
		def conv_sub_func(match):
			return sub_func(match, v)
		
		markdown = re.sub(self.RE_COMMENTS, conv_sub_func, markdown)
		
		html = Markdown(extensions=[GithubFlavoredMarkdownExtension()]).convert(markdown)
		
		if not ignore_content:
			v.variables["content"] = html
		
		return v
