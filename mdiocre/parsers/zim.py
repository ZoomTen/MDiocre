'''
Zim parser

There is no way to have comments in the Zim-Wiki markup format, so the format
is as follows:

[mdiocre: variable]
[mdiocre: variable = "Lorem Ipsum"]

In addition, just as <pre> blocks needs to have a \'\'\' line before and after
them, raw html needs to have a !!! line before and after them.
'''
from os import path as osp
import re
from . import BaseParser, sub_func

class ZimParser(BaseParser):
	'''
	Zim wiki markup parser.
	'''
	
	FILETYPES = ["zim"]
	
	RE_COMMENTS = re.compile(r'\[mdiocre:(.+?)\]')
	
	def convert_markup(self, markup):
		# read line by line
		MARKUP = markup.split('\n')
		
		P_ADD_RE = re.compile(r'^[^=\*\s]')
		
		TAGS_AROUND = {
		# Zim RE's
			'code': "''(?!')(.+?)''",
			'strong'  : '\*\*(?!\*)(.*?)\*\*',
			'em'  : "//(?!/)(.*?)(?<!:)//",
			'u'  : "__(?!_)(.*?)__",
			'del': "~~(?!~)(.+?)~~"
		}
		
		HEADERS_AROUND = {
			'h1': "======",
			'h2': "=====",
			'h3': "====",
			'h4': "===",
			'h5': "=="
		}
		
		LINK_RE = re.compile(r'\[\[(?!\[)((.*?)\|(.*?)|(.*?))\]\]')
		IMG_RE = re.compile(r'\{\{(.*?)\?(.*?)\}\}|\{\{(.*?)\}\}')
		PRE_RE = re.compile(r"^'''\s*$")
		HTML_RE = re.compile(r"^!!!\s*$")
		
		pre_flag = False
		html_flag = False
		ul_flag = False
		output_markup = []
		
		def link_sub(match):
			pipe_txt = match.groups()[2]
			
			link_out = '<a href="{}">{}</a>'
			
			if pipe_txt:
				link = match.groups()[1]
			else:
				link = match.groups()[0]
		
			if not re.search(r'^\w+://', link.lower()):
				if osp.splitext(link)[-1] == '':
					link = link + '.html'
				if link.startswith('+'):
					link = link[1:]
			#elif link.startswith(':'):
			#	link = '../' + link[1:]
			
			if pipe_txt:
				return link_out.format(
					link,
					pipe_txt
				)
			else:
				return link_out.format(
					link,
					link
				)
		
		def img_sub(match):
			img_src = match.groups()[2]
			
			img_out = '<img src="{}" {} />'
			
			if img_src:
				return img_out.format(
					img_src,
					''
				)
			else:
				return img_out.format(
					match.groups()[0],
					match.groups()[1]
				)
		
		for i in range(len(MARKUP)):
			line = MARKUP[i]
			# don't parse header lines
			if not re.search(r'^(Content-Type|Wiki-Format|Creation-Date)', line):
				if re.match(PRE_RE, line):
					pre_flag = not(pre_flag)
					if pre_flag:
						output_markup.append('<pre>')
					else:
						output_markup.append('</pre>')
				elif re.match(HTML_RE, line):
					html_flag = not(html_flag)
				else:
					if pre_flag:
						# don't process anything if we're in
						# pre mode, except to replace HTML chars
						# with escape chars
						line = line.replace('<', '&lt;')\
							.replace('>', '&gt;')
					elif html_flag:
						# absolutely don't process anything
						pass
					else:
						# do processing
						
						# escape chars
						line = line.replace('<', '&lt;')\
							.replace('>', '&gt;')
						
						# special chars
						line = line.replace('©', '&copy;')\
							.replace('®', '&reg;')\
							.replace('™', '&trade;')
						
						# add paragraph tags
						if re.search(P_ADD_RE, line):
							line = '<p>' + line
							line += '</p>'
						
						# links
						# no automatic url matching for now
						line = re.sub(LINK_RE, link_sub, line)
						
						# images
						line = re.sub(IMG_RE, img_sub, line)
						
						# unordered lists
						if re.match("^\* ", line):
							if not ul_flag:
								ul_flag = True
								output_markup.append('<ul>')
							line = re.sub("^\* (.*?)$", '<li>\g<1></li>', line)
						else:
							if ul_flag:
								ul_flag = False
								output_markup.append('</ul>')
						
						
						# basic markup
						for tag, re_ in TAGS_AROUND.items():
							line = re.sub(
								re_,
								'<{0}>\g<1></{0}>'.format(tag),
								line
								)
						
						# header markup
						for tag, markup in HEADERS_AROUND.items():
							line = re.sub(
								'{0} (.*?) {0}$'.format(markup),
								'<{0}>\g<1></{0}>'.format(tag),
								line
								)
					output_markup.append(line)
		
		# lists are mutable in python
		# filter out empty lines, except inside a <pre> block
		pre_mode = [False]
		def not_empty(line, pre_mode):
			if line == '<pre>':
				pre_mode[0] = True
			elif line == '</pre>':
				pre_mode[0] = False
			if pre_mode[0]:
				return True
			else:
				return not re.match(r'^\s*$', line)
		
		return '\n'.join(filter(lambda line: not_empty(line, pre_mode), output_markup))
	
	def to_variables(self, zimtxt, v, ignore_content=False):
		def conv_sub_func(match):
			return sub_func(match, v)
		
		zimtxt = re.sub(self.RE_COMMENTS, conv_sub_func, zimtxt)
		
		html = self.convert_markup(zimtxt)
		
		if not ignore_content:
			v.variables["content"] = html
		
		return v
