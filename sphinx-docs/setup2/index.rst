Quick Setup Guide
=================
TL;DR
-----
* Create a ``mdiocre.ini`` configuration file. It should look like this:
.. code-block:: dosini

   [mdiocre]
   detail = True
   config = site/conf.ini
   logfile= site/run.log

   [build]
   include-html = False
   copy-html = False
   build-exclude = none
   use-prefix = False

   [clean]
   clean-exclude = none
   clean-index = True

* Create a new directory for your site, called ``site``.

* Inside the ``site`` folder, create a new file named ``conf.ini``, which looks like this:
.. code-block:: dosini

   [config]
   modules         = root, blog
   use-templates   = main
   no-index        = none
   source-folder   = site/_src
   build-folder    = site/_html
   template-folder = site/_templates

   [vars]
   site-name       = A MDiocre Powered Site

* Create these folders inside the ``site`` folder: ``_src``, ``_templates``.

* Go inside the ``_src`` folder and create ``index.md``:
.. code-block:: markdown

   <!--title="Home Page"-->
   # Welcome to <!--var:site-name-->!
   
   I hope you enjoyed your stay!
   Here's my [blog](blog/index.html)!

* Go back to ``site``, then inside the ``_templates`` folder create the file ``main.html``:
.. code-block:: html

   <html>
   <head>
   <title><!--var:site-name--> : <!--var:title--></title>
   </head>
   <body>
   <!--var:content-->
   </body>
   <html>
   
* Go back to ``site``, then go inside the ``_src`` folder. Create a new folder called ``blog``.

* Inside the ``blog`` folder, make a file called ``my_first_blog.md``
.. code-block:: markdown

   <!--title="Blog: Everything's boring"-->
   <!--date="2019-03-07"-->
   # Everything's boring
   
   I had a bad day lmao

* Create a file called ``index.template`` in the same folder:
.. code-block:: markdown

   <!--title="Blog: Index"-->
   # Blog
   
   Check out my ramblings.
   
   <!--var:content-->

* Go up three folders, open a terminal and mash ``./mdiocre_console.py build``

* Done. Now have a look at your HTML masterpiece. :)
   