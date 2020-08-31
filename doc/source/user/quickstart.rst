Quickstart
==========

This is a quick guide to setting up a static site with MDiocre 3.0.

Content
-------
Consider this standard Markdown document, which we want to turn into a format
which MDiocre can parse.

.. code-block:: md

   # Markdown for websites?
   
   ## What's a Markdown?
   
   [Markdown](https://daringfireball.net/projects/markdown/) is a simple and
   widely-used way to write structured text with
   headers, lists, paragraphs, etc. It was devised as easily-readable
   syntax for viewing both as raw text file and one that also looks nice when
   converted to HTML.
   
   ## What do I want?
   
   It would be nice if I can make an entire website with Markdown. I don't want
   anything really big and complicated, I just want to write some content and
   then string it all together with some HTML.
   
   I also would want it to be automated, since then I wouldn't have a hard time
   changing anything from my website template. I would also want it to play nice
   with existing tools.
   
   ## What do I need to do?
   
   1. **Think** of how the design will look like. Functions, interfaces, etc.
   2. **Refine** the idea I came up with.
   3. **Implement** the actual thing in the form of a script or compiled program.
   4. **Fix** any bugs and unintended complications
   5. **Publish** even if no one's bothering to look at it.

Add this line at the very top:

.. code-block:: html

   <!--: mdiocre-template = "../template.html" -->

This is the only line that would qualify it to be parsed by MDiocre, it is
simply a link to a template file which is currently nonexistent, but we'll
create it shortly.

We would also like to make the first heading also be the page title, a.k.a
the thing that shows up as the window title, so we'll turn that to a :doc:`variable <variables>`:

.. code-block:: html

   <!--: Article title = "Markdown for websites?" -->

Add that right after, and then replace ``# Markdown for websites?`` with this:

.. code-block:: md

   # <!--: Article title -->

This variable will also be read by the template and apply it as the page title.

In a directory of your choosing, create a folder. Inside that folder, create
another folder named `source` and save this as `index.md`.

Template
--------

Outside the source folder, create ``template.html``:

.. code-block:: html
   
   <html>
       <head>
           <title><!--: Article title --></title>
       </head>
       <body>
           <!--: content -->
       </body>
   </html>

The ``<!--: content -->`` line is where the converted Markdown will go.

Compiling
---------

Run the following:

.. code-block::

   python3 mdiocre.py source built

You should see the following output:

.. code-block::

	MDiocre version 3.0 (2020-08-30)
	================================

	...create:<your directory here>/built
	    ...index.md is a MDiocre file, writing index.html

If you look inside the `built` directory, you should see the processed `index.html`
page.

The neat thing about MDiocre is that just the files that MDiocre consider worthy
of conversion will be converted, but everything else stays the same 1:1 with the
source version.

That also means templates, styles should be separated from the source directory,
so the source directory would only contain pages and their files.
