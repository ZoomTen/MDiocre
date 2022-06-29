import re
import random
import xml.etree.ElementTree as ET
from . import BaseParser, sub_func

class GemParser(BaseParser):
	'''
	Gemtext parser. Comments are parsed the same way as Zim does
	'''
	
	FILETYPES = ["gmi", "gem"]

	RE_COMMENTS = re.compile(r'\[mdiocre:(.+?)\]')
	
	def convert_markup(self, markup):
		# read line by line
		MARKUP = markup.split('\n')
		P_ADD_RE         = re.compile(r'^(?!#|\*|>|```|=>)(.+)$')
		HEADINGS_RE      = re.compile(r'^(#{1,6})\s+(.+)$') # spec says mandatory space chara
		LINKS_RE         = re.compile(r'^=>\s*(\w+:?/?/?[^\s]+)(\s+(.+$))?')
		PREFORMATTED_RE  = re.compile(r'^```(.+)$')
		ULIST_RE         = re.compile(r'^\*\s+(.+)$')
		LINKS_INSIDE     = re.compile(r'\(=>\s*(\w+:?/?/?[^\s]+)(\s+(.+?))?\)') 
		BLOCKQUOTE_RE    = re.compile(r'^>\s+(.+)$')
		
		output_markup = []
		lists_mode = {
			'ul': False,
			'ol': False
		}
		pre_mode = False
		cur_code_hash = ''
		code_alts = {}
		
		def make_code_hash():
			new_key = '__code__'
			for i in random.randbytes(32):
				new_key += hex(i)[2:]
			return new_key
		
		for i in range(len(MARKUP)):
			line = MARKUP[i]
			
			if not pre_mode: # standard text
				# add paragraph tags
				if re.search(P_ADD_RE, line):
					line = '<p>' + line + '</p>'
				
				# add header tags
				line = re.sub(HEADINGS_RE,
					lambda a: "<h%d>%s</h%d>" % (len(a.group(1)), a.group(2), len(a.group(1))),
					line
				)
				
				# add blockquotes
				line = re.sub(BLOCKQUOTE_RE,
					lambda a: "<blockquote>%s</blockquote>" % (a.group(1)),
					line
				)
				
				is_list_or_link_set = (bool(re.match(ULIST_RE, line)) or bool(re.match(LINKS_RE, line)))
				
				# lists
				if re.match(ULIST_RE, line):
					if not lists_mode['ul']:
						lists_mode['ul'] = True
						output_markup.append('<ul>')
					line = re.sub(ULIST_RE,
						lambda a: "<li>%s</li>" % (a.group(1)),
						line
					)
				
				if not is_list_or_link_set:
					if lists_mode['ul']:
						lists_mode['ul'] = False
						output_markup.append('</ul>')
				
				# links
				def gen_link(result):
					link_str = '<a href="%s">%s</a>'
					if result.group(3):
						return link_str % (result.group(1), result.group(3))
					# no unique txt
					return link_str % (result.group(1), result.group(1))
				
				# links on its own is treated like lists
				if re.match(LINKS_RE, line):
					if not lists_mode['ul']:
						lists_mode['ul'] = True
						output_markup.append('<ul class="gemtext-links">')
					line = "<li>%s</li>" % (re.sub(LINKS_RE, gen_link, line))
				
				line = re.sub(LINKS_INSIDE, gen_link, line)
				
				if re.match(PREFORMATTED_RE, line):
					cur_code_hash = make_code_hash()
					line = '<pre alt="%s"><code>' % (cur_code_hash)
					pre_mode = True
				
				if False: # comment out this line to literally render blank lines as <br>
					if len(line.strip()) == 0:
						line = '<br>'
			else: # preformatted text
				code_end = re.match(PREFORMATTED_RE, line)
				if code_end:
					line = '</code></pre>'
					pre_mode = False
					if code_end.group(1):
						code_alts[cur_code_hash] = code_end.group(1)
			
			output_markup.append(line)
		output_str = '\n'.join(output_markup)
		
		# resolve code alt text
		for key, value in code_alts.items():
			output_str = output_str.replace(key, value)
		
		return output_str
	
	def to_variables(self, html, v, ignore_content=False):
		def trf_sub_func(match):
			return sub_func(match, v)
		
		# do substitution...
		gmitxt = re.sub(self.RE_COMMENTS, trf_sub_func, html)
		
		html = self.convert_markup(gmitxt)
		# escape all text
		etr = ET.fromstring("<_doc_>%s</_doc_>" % html)
		html = '\n'.join(
			ET.tostring(etr, encoding='unicode', method='html')\
			.split('\n')[1:-1]
		)
		
		if not ignore_content:
			v.variables["content"] = html
			
		return v
