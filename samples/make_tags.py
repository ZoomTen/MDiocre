'''
Make a page for each tag

NOTE: tags are defined in a variable called "tags", and are space-separated.
      tags are also case-sensitive!
'''

import os
import sys
# point this to the folder where mdiocre.py is located
sys.path.append(os.path.abspath('..'))

import datetime
from mdiocre.core import MDiocre
from mdiocre.wizard import Wizard

# directory where the blog files are
BLOG_DIR = "source/blog"

# where the generated files will be
OUT_DIR = "tags"

# use "" for no prefix
TAG_PREFIX = "tag_"

# which template to use
TAGS_TEMPLATE = "source/blog/template.html"

if __name__ == '__main__':
	# set up MDiocre and file list
	m = MDiocre()
	blog_files = [i for i in os.listdir(BLOG_DIR) \
		      if \
		      (i.lower().endswith('.md') or i.lower().endswith('.rst'))
		      and not os.path.splitext(i.lower())[0].startswith('index')]
	
	tags = {}
	
	# make entry for each file
	for f in blog_files:
		file_path = os.path.join(BLOG_DIR, f)
		file_name, file_ext = os.path.splitext(f)
		
		# find suitable converter
		file_ext = file_ext[1:].lower()
		m.switch_parser(Wizard.converters[file_ext])
		
		# read file
		with open(file_path, 'r') as content:
			content_vars = m.process(content.read(), ignore_content=True)
		
		date  = content_vars.variables['date']
		title = content_vars.variables['title']
		page_tags = content_vars.get('tags').strip()
		
		if page_tags == '':
			page_tag_list = ['unsorted']
		else:
			page_tag_list = [x.strip() for x in page_tags.split(' ')]
		
		for tag in page_tag_list:
			try:
				tags[tag].append((date, title, file_name))
			except KeyError:
				tags[tag] = []
				tags[tag].append((date, title, file_name))
	
	for tag in tags:
		tags[tag].sort(key=lambda entry: datetime.datetime.strptime(entry[0], "%Y-%m-%d"))
		tags[tag].reverse() # comment this out if you want to sort by oldest
	
	# get template
	with open(TAGS_TEMPLATE, 'r') as t:
		template = t.read()
	
	# create tags page in markdown
	m.switch_parser('markdown')
	
	# create tags directory
	os.makedirs(OUT_DIR, exist_ok=True)
	
	for tag_name, tag_list in tags.items():
		entries = ["# Tag '{}'\n".format(tag_name)]
		for entry in tag_list:
			entries.append('* **{}** - [{}]({}.html)'.format(entry[0], entry[1], entry[2]))
		
		page_contents = '\n'.join(entries)
		
		gen_vars = m.process(page_contents)
		
		new_page = m.render(template, gen_vars)
		
		file_name = '{}{}.html'.format(TAG_PREFIX, tag_name)
		
		with open(os.path.join(OUT_DIR, file_name), 'w') as out_file:
			out_file.write(new_page)
			print('wrote {}'.format(file_name))
