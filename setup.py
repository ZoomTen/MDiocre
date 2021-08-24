import os
import re
from distutils.util import convert_path
from versioning import get_git_version

def readme():
	with open('README.md', 'r', encoding='utf-8') as rf:
		return rf.read()

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(
	name='mdiocre',
	version=get_git_version(),
	description='Static website generator',
	long_description=readme(),
	long_description_content_type='text/markdown',
	license='MIT',
	author='Zumi Daxuya',
	author_email='daxuya.zumi+mdiocre@protonmail.com',
	url='https://zumi.neocities.org/stuff/mdiocre',
	packages=['mdiocre', 'mdiocre.parsers', 'mdiocre.interface'],
	keywords=['converter', 'generator', 'markdown', 'html', 'static'],
	install_requires=['markdown', 'py-gfm'],
	entry_points={
		'console_scripts':
			[
				'mdiocre = mdiocre.interface.cli:cli'
			]
	},
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Natural Language :: English',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Topic :: Software Development :: Libraries :: Python Modules',
	]
)
