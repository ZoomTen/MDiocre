Creating templates
======================

First, check your `template-folder` settings in
``mdiocre.ini``. This setting is set relative to the MDiocre
install directory, so, for example, if you have
MDiocre installed in ``C:\MDiocre`` and `template-folder` is set to ``_templates``, then it will look for templates in ``C:\MDiocre\_templates``.

Site templates
----------------
Simple enough, these templates are used to define
the look and feel of a site. They are written in
HTML and they can contain variables.

These are the templates that will reside in the
`template-folder`, and as such MDiocre will use
a template of your choosing from this directory.

Say you've set several modules in ``mdiocre.ini``,
for example `root`, `blog`, and `projects`. If
you have only specified `x` as the only
template used, MDiocre will use it for all of them.

However, if you tell it to use `x`, `y`, and `z`, the module `root` will use template `x`, `blog`
will use `y`, and `projects` will use `z`.

.. todo:: Work out cases in which the number of templates listed **does not** match the number of
   modules listed, except n=1.

Anyway, let's start. Create a folder (it doesn't
exist) called ``_templates`` and check ``_conf/sample.ini`` if we did point to that folder.

Open up Notepad (or any other text editing tool)
and type this:

.. code-block:: html

   <html>
   <head>
       <title><!--var:title--> - <!--var:site-name--></title>
   </head>
   <body>
       <!--var:content--> 
   </body>
   </html>

Save this file in that folder, call it ``main.html``.
This is a simple page template that will display the page
title and site name on the browser's titlebar, as well
as displaying the actual content on the window.

Of course, if you know HTML, you can pretty much go
nuts on the design, feel free to experiment. But
don't touch the title and the "var content" stuff
there yet - I'll explain it later!

Index templates
---------------

Aha, just to complicate things even further, we have *index templates*. These are module-specific templates for setting the content of an index page. Things like putting an introductory paragraph, notes at the bottom of the page list, etc. etc.

Unlike *site-templates*, these are written in Markdown!

.. todo:: explain a bit more, also write that root ignores
   index template

Create the project and pages subfolders in your source path...

.. todo:: Cover simple templates and the index.template on every directory.
.. todo:: Also cover vars as explained in mdiocre.Wizard