#!/usr/bin/python

CLI_VERSION = '1.0.1'

from argparse import ArgumentParser
from mdiocre.__meta__ import __version__ as MD_VERSION
from mdiocre.wizard import Wizard

import logging
import sys

def has_color():
	'''
	Borrowed from the `Django <https://github.com/django/django>`_ project.
	
	Returns:
	    True if the running system's terminal supports color, and False
	    otherwise.
	'''
	is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
	return is_a_tty

class MDiocreHandler(logging.Handler):
	quiet = False
	
	def set_quiet(self, quiet):
		self.quiet = quiet
		return self
	
	def emit(self, record):
		if not self.quiet:
			color_enable = has_color()
			if color_enable:
				if record.levelno >= 35: # SERIOUS, ERROR, CRITICAL
					print('\033[31m', end='')
				elif record.levelno >= 30: # WARNING
					print('\033[33m', end='')
				elif record.levelno >= 25: # INFO + 5, a.k.a. OK
					print('\033[32m', end='')
				else:
					print('\033[0m', end='')
			
			sep = '... '
			
			if not color_enable:
				sep = '\n[{}] '.format(record.levelname.split(':')[0])
			
			print(''.join(['    '*int(record.levelno % 5), sep, record.msg]), end='')
			
			if color_enable:
				print('\033[0m')

def cli():
	ap = ArgumentParser(
			description='A terrible static page generator.'
		)

	ap.add_argument('source_dir', help='Webpages source directory')
	ap.add_argument('build_dir', help='Output directory')
	ap.add_argument('--quiet', '-q', help='No output', action='store_true')

	args = ap.parse_args()

	w = Wizard()
	
	logger = logging.getLogger('mdiocre')
	logger.addHandler(MDiocreHandler().set_quiet(args.quiet))
	logger.setLevel(logging.DEBUG)
	
	# display header
	if not args.quiet:
		print()
		app_str  = "MDiocre-CLI version {}".format(CLI_VERSION)
		base_str = "(using MDiocre version {})".format(MD_VERSION)
		print(app_str)
		print('-'*len(app_str))
		print(base_str)

	# run the wizard
	w.register_converters()
	w.generate_from_directory(vars(args))
	
	print()

if __name__ == '__main__':
	cli()
