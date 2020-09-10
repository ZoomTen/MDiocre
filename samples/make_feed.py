'''
Create an RSS feed 
'''
from mdiocre.core import MDiocre
from mdiocre.wizard import Wizard
from feedgen import feed
import re

# directory where the blog files are
BLOG_DIR = "source/blog"
WEBSITE_NAME = "My Website"
WEBSITE_AUTHOR = "Joe Bloggs"
WEBSITE_LANG = "en"
AUTHOR_EMAIL = "something@example.com"

WEBSITE_LINK = 'http://example.com'
RSS_LINK = 'http://example.com/feed.rss'

if __name__ == '__main__':
	

	# feed info
	fg = feed.FeedGenerator()
	fg.title(WEBSITE_NAME)
	fg.author( {'name':WEBSITE_AUTHOR,'email':AUTHOR_EMAIL} )
	fg.language(WEBSITE_LANG)
	fg.generator('python-feedgen (MDiocre v.3.0)')

	# feed links
	fg.link(href=WEBSITE_LINK)
	fg.link(href=RSS_LINK, rel='self', type='application/rss+xml')

	# set up MDiocre and file list
	m = MDiocre()
	blog_files = [i for i in os.listdir(BLOG_DIR) \
		      if \
		      (i.lower().endswith('.md') or i.lower().endswith('.rst'))
		      and not os.path.splitext(i.lower())[0].startswith('index')]

	# make entry for each file
	for f in blog_files:
		file_path = os.path.join(BLOG_DIR, f)
		file_name, file_ext = os.path.splitext(f)
		
		# find suitable converter
		file_ext = file_ext[1:].lower()
		m.switch_parser(Wizard.converters[file_ext])
		
		# read file
		with open(file_path, 'r') as content:
			content_vars = m.process(content.read())
		
		# prepare feed entry
		fe = fg.add_entry()
		
		# set title, defined by e.g. <!--:title = "My First Blog Post" -->
		if content_vars.get('title') != '':
			blog_title = content_vars.get('title')
		else:
			blog_title = file_name
		
		# set date, defined by e.g. <!--:date = "2020-09-09" -->
		blog_pub = content_vars.get("date")
		
		# fill feed entry
		fe.title(blog_title)
		fe.description(blog_content)
		fe.link(href="{}/{}.html".format(WEBSITE_LINK, file_name))
		fe.published(blog_pub)

	# print out the rss feed
	print(fg.rss_str(pretty=True).decode(encoding='utf-8'))
