import shutil
import os
import re
from .utils import declare, Logger
from .core import MDiocre

'''
Automatic page generation tools that require manipulating the file system
'''

l = Logger()
m = MDiocre()

class Wizard():
	def __init__(self):
		pass
	
	def is_mdiocre_string(self, md_string):
		'''
		Determines whether or not this is valid MDiocre-formatted
		markdown.
		
		The only criteria currently needed for this is whether or not
		it contains a ``mdiocre_template`` variable, and whether or
		not that ends in ``.html``.
		
		Args:
		    md_string(string): The markdown-formatted text to validate.
		
		Returns:
		    True if it is a valid string, False otherwise.
		
		'''
		variables = m.process(md_string, ignore_content=True)
		
		md_template_string = variables.get('mdiocre_template')
		
		if md_template_string != '':
			if md_template_string.lower()[-5:] == '.html':
				return True
		return False
	
	def generate_from_string(self, md_string, root):
		'''
		Given a MDiocre string and a "root" path, convert it to a proper
		HTML document.
		
		MDiocre is simple: HTML template + Markdown = New HTML page
		
		The HTML template itself is obtained from the presence of the
		``mdiocre_template`` variable, which simply contains the path
		of the template file relative to the ``root`` set here. Which is
		why the ``mdiocre_template`` variable must be present for the
		markdown to be considered convertable by MDiocre.
		
		Args:
		    md_string(string): The markdown-formatted text to convert.
		    root(string): The 'root' path.
		
		Returns:
		    A rendered HTML string. If the ``md_string`` is invalid or if
		    it cannot find the template file, it will return an empty string.
		'''
		if self.is_mdiocre_string(md_string):
			variables = m.process(md_string)
			
			template_file = os.path.abspath(
						os.path.sep.join([
							root,
							variables.get('mdiocre_template')
						])
					)
			
			if os.path.exists(template_file):
				with open(template_file, 'r') as tf:
					template = tf.read()
					return m.render(template, variables)
			else:
				return ''
		else:
			# return an empty string from the get-go if it isn't
			# a valid mdiocre file
			return ''
		

	def generate_from_directory(self, args):
		'''
		Generates pages based on the directory it is supplied through
		`args`.
		
		This function looks at the files inside ``source_dir`` recursively
		and copies the files to ``build_dir``, or generates a page if it
		is a markdown file.
		
		In order to generate pages, it needs a template. The template
		directory is supplied through the ``mdiocre_template`` variable,
		and it is relative to ``source_dir``.
		
		Args:
		    args (dict): A dictionary containing arguments for this
		        function. It should have the following keys:
		        ``source_dir`` and ``build_dir``.
		
		Returns:
		    True, if every file is successfully processed. Otherwise,
		    return False. Additionally, it will also create or modify
		    files on the filesystem.
		'''
		# type checking
		declare(args, dict)
		
		source_dir = os.path.abspath(args['source_dir'])
		build_dir = os.path.abspath(args['build_dir'])
		
		source_parent, source_folder = os.path.split(source_dir)
		
		# process files from the source directory
		for path, folders, files in (os.walk(source_dir)):
			parent_path, path_folder = os.path.split(path)
			
			if parent_path == source_parent:
				target_path = build_dir
			else:
				target_path = os.path.abspath(
						os.path.sep.join([
							build_dir,
							parent_path[len(source_dir):],
							path_folder
							])
						)
			
			# make directories
			l.print('create:', target_path)
			
			try:
				os.makedirs(target_path)
			except FileExistsError:
				l.print('directory exists -- making anyway!', severity='warning')
				os.makedirs(target_path, exist_ok=True)
			
			# copy files in directory to their respective
			# counterparts, but check .md files
			for f in files:
				original_file = os.path.sep.join([path, f])
				target_file = os.path.sep.join([target_path, f])
				
				# markdown file ending in .md -> html
				# needs a template file ending in .html
				if f.lower()[-3:] == '.md':
					# new target file name
					convert_file = target_file[:-3] + '.html'
					
					# process file
					with open(original_file, 'r') as md:
						orig_md = md.read()
					
					conv_md = self.generate_from_string(orig_md, source_dir)
					
					if conv_md != '':
						# if properly converted, write the
						# html file
						if os.path.exists(convert_file):
							l.print('(OVERWRITING {})'.format(os.path.split(convert_file)[1]),
								level=1, severity='serious')
						l.print('{} is a MDiocre file, writing {}'.format(f, os.path.split(convert_file)[1]),
							level=1)
						with open(convert_file, 'w') as rendered:
							rendered.write(conv_md)
					else:
						# if not, don't convert - just perform a copy
						if os.path.exists(target_file):
							l.print('(OVERWRITING {})'.format(f),
								level=1, severity='serious')
						l.print('{} is NOT a MDiocre file, copying instead'.format(f),
							level=1, severity='warning')
						shutil.copyfile(
							original_file,
							target_file
							)
				# html, jpg, png, txt, etc.
				else:
					if os.path.exists(target_file):
						l.print('(OVERWRITING {})'.format(f),
							level=1, severity='serious')
					l.print('Copying {}'.format(f),
						level=1)
					shutil.copyfile(
						original_file,
						target_file
						)
			
