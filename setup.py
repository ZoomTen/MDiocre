import os
import re
from distutils.util import convert_path

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

META_PATH = 'mdiocre/__meta__.py'

def get_meta(meta_path, key):
	meta_file = open(convert_path(meta_path)).read()
	meta_match = re.search("^__{}__\s*=\s*['\"]([^'\"]*)['\"]".format(key), meta_file, re.M)
	if meta_match:
		return meta_match.group(1)
	raise RuntimeError('Unable to find meta string.')

version = get_meta(META_PATH, 'version')

setup(
	name='mdiocre',
	version=version,
	description='Static website generator',
	license='MIT',
	author='Zumi Daxuya',
	author_email='daxuya.zumi+mdiocre@protonmail.com',
	url='https://github.com/ZoomTen/MDiocre',
	packages=['mdiocre', 'mdiocre.parsers'],
	keywords=['converter', 'generator', 'markdown', 'html', 'static'],
	install_requires=['markdown'],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Natural Language :: English',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.8',
		'Topic :: Software Development :: Libraries :: Python Modules',
	]
)
