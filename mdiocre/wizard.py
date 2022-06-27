import shutil
import os
import re
from .utils import declare
import logging
from .core import MDiocre

'''
Automatic page generation tools that require manipulating the file system
'''

logger = logging.getLogger('mdiocre.wizard')

# log levels
log_info    = logging.INFO
log_ok      = log_info + 5
log_warning = logging.WARNING
log_serious = log_warning + 5
log_error   = logging.ERROR

class Wizard():
	# TODO: move this list to core.py, have all the converters register to core
	converters = {'md'   : 'markdown',
	              'rst'  : 'rst',
	              'html' : 'html',
	              'htm'  : 'html',
	              'zimtxt'  : 'zim',
	              'gem'  : 'gem',
	              'gmi'  : 'gem',
	              }

	def __init__(self):
		self.m = MDiocre()
	
	def register_converter(self, file_extension, parser_name):
		'''
		Registers a parser with a file extension.
		'''
		# type checking
		declare(file_extension, str)
		declare(parser_name, str)
		
		self.converter[file_extension] = parser_name
		print('.{} = {}'.format(file_extension, parser_name))
	
	def vars_directly_from_file(self, source_file):
		'''
		Generate a VariableManager object directly from a source file
		name using automatic file type detection. Directly means that
		it won't check if it is a "valid" MDiocre file - that is,
		whether or not there is a template doesn't matter one bit.
		
		Args:
		    source_file(string): Path to the MDiocre file to process.
		
		Returns:
		    VariableManager object if the source_file is parseable.
		    None otherwise.
		'''
		# type checking
		declare(source_file, str)
		
		# check file extension
		source_name, source_ext = os.path.splitext(source_file)
		
		# lop off the dot and make it all lowercase
		source_ext = source_ext[1:].lower()
		
		source_dir, source_filename = os.path.split(source_file)
		
		if source_ext in self.converters:
			self.m.switch_parser(self.converters[source_ext])
			
			with open(source_file, 'r') as orig:
				orig_string = orig.read()
			
			return self.m.process(orig_string)
		
		return None
		
	def is_mdiocre_string(self, md_string):
		'''
		Determines whether or not this is valid MDiocre-formatted
		markdown.
		
		The only criteria currently needed for this is whether or not
		it contains a ``mdiocre-template`` variable.
		
		Args:
		    md_string(string): The markdown-formatted text to validate.
		
		Returns:
		    True if it is a valid string, False otherwise.
		
		'''
		# type checking
		declare(md_string, str)
		
		variables = self.m.process(md_string, ignore_content=True)
		
		md_template_string = variables.get('mdiocre-template')
		
		if md_template_string != '':
			# XXX: templates are only HTML
			# if md_template_string.lower()[-5:] == '.html':
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
		why the ``mdiocre-template`` variable must be present for the
		markdown to be considered convertable by MDiocre.
		
		Args:
		    md_string(string): The markdown-formatted text to convert.
		    root(string): The 'root' path.
		
		Returns:
		    A rendered HTML string. If the ``md_string`` is invalid or if
		    it cannot find the template file, it will return an empty string.
		'''
		# type checking
		declare(md_string, str)
		declare(root, str)
		
		if self.is_mdiocre_string(md_string):
			variables = self.m.process(md_string)
			
			template_file = os.path.abspath(
						os.path.sep.join([
							root,
							variables.get('mdiocre-template')
						])
					)
			
			if os.path.exists(template_file):
				with open(template_file, 'r') as tf:
					template = tf.read()
					return self.m.render(template, variables)
			else:
				return ''
		else:
			# return an empty string from the get-go if it isn't
			# a valid mdiocre file
			return ''
	
	def generate_from_path(self, source_file, built_file, root='', to_html=False, level=0):
		'''
		If the file is a MDiocre file, generate an HTML page from a
		source file to a built file. Otherwise, simply copy the file.
		'''
		# type checking
		declare(source_file, str)
		declare(built_file, str)
		declare(root, str)
		declare(to_html, bool)
		
		# check file extension
		source_name, source_ext = os.path.splitext(source_file)
		
		# lop off the dot and make it all lowercase
		source_ext = source_ext[1:].lower()
		
		source_dir, source_filename = os.path.split(source_file)
		built_dir, built_filename = os.path.split(built_file)
		
		has_file_originally = os.path.exists(built_file)
		
		if source_ext in self.converters:
			try:
				self.m.switch_parser(self.converters[source_ext])
				with open(source_file, 'r') as orig:
					orig_string = orig.read()
				
				conv = self.generate_from_string(orig_string, root)
				
				if conv != '':
					if to_html:
						built_name, built_ext = os.path.splitext(built_file)
						built_file = os.path.extsep.join([built_name, 'html'])
						
						# update with the html name
						has_file_originally = os.path.exists(built_file)
						
						built_dir, built_filename = os.path.split(built_file)
					# if properly converted, write the file
					logger.log(log_ok + level, '{} is a MDiocre file, writing {}.'.format(source_filename, built_filename))
					with open(built_file, 'w') as rendered:
						rendered.write(conv)
				else:
					# if not, don't convert - just perform a copy
					logger.log(log_warning + level, '{} is NOT a MDiocre file, copying instead.'.format(source_filename, built_filename))
					shutil.copyfile(
						source_file,
						built_file
						)
			except Exception as e:
				logger.log(log_error + level, "{}: an error occured, copying file instead...".format(source_filename))
				logger.log(log_error + level + 1, "{}".format(e))
				shutil.copyfile(
					source_file,
					built_file
					)
		else:
			logger.log(log_info + level, 'copying {}'.format(source_filename))
			shutil.copyfile(
				source_file,
				built_file
				)
		
		if has_file_originally:
			logger.log(log_serious + level,'overwriting {}!'.format(built_filename))

	def generate_from_directory(self, args, callback=None):
		'''
		Generates pages based on the directory it is supplied through
		`args`.
		
		This function looks at the files inside the `args`' ``source_dir`` path recursively
		and copies the files to ``build_dir``, or generates a page if it
                is a MDiocre file (see :meth:`is_mdiocre_string`).
		
		In order to generate pages, it needs a template. The template
		file is supplied through each file's ``mdiocre-template`` variable,
		and it is relative to ``source_dir``.
		
		Args:
		    args (dict): A dictionary containing arguments for this
		        function. It must have the following keys:
		        ``source_dir`` and ``build_dir``.
		    callback (func): A function to call every file completion.
		        Its arguments are a dictionary containing the keys
		        "original_file", "target_file", "root".
		
		Returns:
		    True, if every file is successfully processed. Otherwise,
		    return False. Additionally, it will also create or modify
		    files on the filesystem.
		'''
		# type checking
		declare(args, dict)
		
		source_dir = os.path.abspath(args['source_dir'])
		build_dir = os.path.abspath(args['build_dir'])
		
		sd_rel = os.path.relpath(source_dir)
		bd_rel = os.path.relpath(build_dir)
		
		source_parent, source_folder = os.path.split(source_dir)
		
		logger.info('begin processing {} -> {}.'.format(sd_rel, bd_rel))
		
		# process files from the source directory
		for path, folders, files in (os.walk(source_dir, followlinks=True)):
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
			
			sp_rel = os.path.relpath(path)
			tp_rel = os.path.relpath(target_path)
			
			# make directories
			
			# prevent the root directory logged twice
			if sd_rel == sp_rel:
				pass
			elif bd_rel == tp_rel:
				pass
			else:
				logger.log(log_info + 1, '{} -> {}.'.format(sp_rel, tp_rel))
			
			try:
				os.makedirs(target_path)
			except FileExistsError:
				logger.log(log_warning + 2, 'directory "{}" exists -- making anyway!'.format(os.path.relpath(target_path)))
				os.makedirs(target_path, exist_ok=True)
			
			# do the conversion
			for f in files:
				original_file = os.path.sep.join([path, f])
				target_file = os.path.sep.join([target_path, f])
				
				original_name, original_ext = os.path.splitext(original_file)
				# lop off the dot and make it all lowercase
				original_ext = original_ext[1:].lower()
				
				self.generate_from_path(original_file, target_file, root=source_dir, to_html=True, level=2)
				
				if type(callback).__name__ == 'function':
					callback({"original_file": original_file,"target_file":target_file,"root":source_dir})
		logger.info('done processing {}.'.format(sd_rel))
