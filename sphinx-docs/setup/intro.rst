Introduction
============
About
-----
Welcome to **MDiocre**, a static website generation system.
It's probably buggy and unstable and has nothing to offer compared
to Jekyll, but for me it's a nice peek into the messy world of
app develompent. *MDiocre* uses `Markdown <https://en.wikipedia.org/wiki/Markdown>`_,
so if you've ever used Discord, Slack, GitHub or anything else that supports it,
this will almost be a piece of cake to use.

Requirements
------------

Definitions
-----------
Here's the nerdspeak we'll be using throughout this document to
refer to a few concepts:

**Static websites**
   Websites that do not use databases or any server-side manipulation
   to change its' content. This is suitable for documentation, blogs
   and articles that are hosted via a web hosting service that do
   not offer advanced services such as PHP support.

**Building**
   The process of compiling raw Markdown files into plain HTML pages you can
   then go and publish to whatever your web host is.
   
**Source directory**
   This is where you will be putting your Markdown documents in. However,
   putting it inside the folder itself will not do anything unless you
   specify that the "root" module must be built in the site configuration.
   Next, if you create subfolders, those should be included as modules
   in the site config. The only downside is, you cannot have a subfolder
   named "root".

**Index, indexing**
   In a module, indexing is essentially creating links to the pages.
   Generated in the form of an unordered list, sometimes with dates and
   titles. During the build process, *MDiocre* will scan the files
   for the date and title of the document and adjusts the entries
   accordingly. See the technical infos for :doc:`../technical/wizard` for more information.

What are Modules?
-----------------
Not to be confused with Python's modules, a "module" is what *MDiocre* calls subdirectories on websites. 

For example, a website domain ``its.dot.com`` has a subfolder called ``articles`` and another called ``docs``, rendered as ``its.dot.com/articles`` and
``its.dot.com/docs``, respectively. In MDiocre, ``articles`` and ``docs`` are *modules* of that domain. To *MDiocre*, a "module" is really just a subfolder within a source directory that will then be compiled into an actual subfolder in a webpage.

Modules can be named however you desire, however
there is a special module called ``root``, which,
as the name might suggest, contains the *root of
the website*. This is where you might have things
such as index.html.

How is MDiocre configured?
--------------------------
There are two types of configuration used in MDiocre:

**Site configuration**
   An `INI file <https://en.wikipedia.org/wiki/INI_file>`_ which contains
   the "recipe" to make a site. This contains things such as telling
   *MDiocre* which modules are present and are supposed to be compiled,
   which templates to use, and which folders are to be used.
   You can make multiple configurations for a number of websites.

**MDiocre configuration**
   Another INI file! It takes the form of the file ``mdiocre.ini`` in the same directory
   that ``mdiocre_console.py`` or ``MDiocre.exe`` resides. Unlike the *site configuration*,
   there can be only one of it that *MDiocre* can read. This would be the
   replacement to using the command line manually, so instead of doing `this <http://i.imgur.com/m62wmVU.png>`_, you can use this file instead. You can use this
   to pick which site configuration to use, how
   verbose should it be, and whether or not to
   log the compilation process, so you would
   be able to know what went wrong. 