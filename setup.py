import os
import re
from distutils.util import convert_path

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

def version_number(filename):
	version_file = open(convert_path(filename)).read()
	version_match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", version_file, re.M)
	if version_match:
		return version_match.group(1)
	raise RuntimeError('Unable to find version string.')

version = version_number('mdiocre/__meta__.py')

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
