'''
Make a paginated index
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
OUT_DIR = "index"

# how many posts per page
PAGINATE_EVERY = 5

# which template to use
INDEX_TEMPLATE = "source/blog/template.html"

if __name__ == '__main__':
	# set up MDiocre and file list
	m = MDiocre()
	blog_files = [i for i in os.listdir(BLOG_DIR) \
		      if \
		      (i.lower().endswith('.md') or i.lower().endswith('.rst'))
		      and not os.path.splitext(i.lower())[0].startswith('index')]
	
	blog_entries = []
	
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
		
		blog_entries.append((date, title, file_name))
	
	blog_entries.sort(key=lambda entry: datetime.datetime.strptime(entry[0], "%Y-%m-%d"))
	blog_entries.reverse() # comment this out if you want to sort by oldest
	
	# split sorted blog entries
	blog_split = [blog_entries[x:x+PAGINATE_EVERY] for x in range(0, len(blog_entries), PAGINATE_EVERY)]
	
	# get template
	with open(INDEX_TEMPLATE, 'r') as t:
		template = t.read()
	
	# create index page in markdown
	m.switch_parser('markdown')
	
	# create index directory
	os.makedirs(OUT_DIR, exist_ok=True)
	
	page_num = 0
	
	for page in blog_split:
		page_num += 1
		
		entries = []
		for entry in page:
			entries.append('* **{}** - [{}]({}.html)'.format(entry[0], entry[1], entry[2]))
		
		page_contents = '\n'.join(entries)
		
		gen_v_ = m.process(page_contents)
		
		page_contents = '<!--: content -->'
		if page_num == 1:
			page_contents += '\n\n* {}\n* [Next](index_{}.html)\n'.format(page_num, page_num+1)
		elif page_num == len(blog_split):
			page_contents += '\n\n* [Previous](index_{}.html)\n* {}\n'.format(page_num-1, page_num)
		else:
			page_contents += '\n\n* [Previous](index_{}.html)\n* {}\n* [Next](index_{}.html)\n'.format(page_num-1, page_num, page_num+1)
		
		page_contents = m.render(page_contents, gen_v_)
		
		gen_vars = m.process(page_contents)
		
		new_page = m.render(template, gen_vars)
		
		file_name = 'index_{}.html'.format(page_num)
		
		with open(os.path.join(OUT_DIR, file_name), 'w') as out_file:
			out_file.write(new_page)
			print('wrote {}'.format(file_name))
