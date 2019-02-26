Installation and Setup
======================

Requirements
---------------
* `Pandoc <https://pandoc.org/installing.html>`_.
   Follow the installation instructions for your OS.

* `Python 3 <https://www.python.org/downloads/>`_.

.. note:: Python 3 is needed to run the source distribution, not the binaries
   (or exe's).
   
      If you are using Linux and other Unix-like systems, I recommend checking
      your distro's package manager first. Additionally, if you are
      running from the sources, you will need to install the
      ``pypandoc`` and ``colorama`` modules through `pip`, using
      a command like ``pip install --user pypandoc colorama``.

Download
--------
In this link you will find two downloads for MDiocre, one is a source
distribution and the other is a "binary" distribution, a.k.a. a file
you can simply run.

The binary distribution is currently only available for Windows, so
if you are using Windows I recommend using that one.

For everyone else, just use the source distributions for now.

Once you have downloaded it, extract the zip into a folder of your
choice.

Configuration
-----------------
Inside the distribution files you have extracted there will be two sample
configurations:

Site Configuration
~~~~~~~~~~~~~~~~~~~~~~~

This is ``conf/sample.ini``, an example of a *site configuration*.

.. code-block:: dosini

   [config]
   modules         = root, pages, projects
   use-templates   = main
   no-index        = none
   source-folder   = _src
   build-folder    = _html
   template-folder = _templates

   [vars]
   site-name       = Your site name

Under the *config* section, you will see the following options:

**modules**
   A comma-separated list of *modules* or subdirectories (within the *source-folder*)
   to compile to HTML at the *build-folder*.
   
**use-templates**
   The name of the page templates to use, so long as it can be found within
   the *template-folder*. Comma-separated, the order of the templates must
   match the order of the modules. For example, if you want ``root`` to have
   the ``velvet`` theme and ``articles`` to have the ``plain`` one, you would
   set *modules* to ``root, articles`` and *use-templates* to ``velvet, plain``.
   If only one template is listed in the option, it will use the template for
   **all** modules.
   
**no-index**
   A comma-separated list of *modules* that are not to be indexed.
   
**source-folder**
   The folder, relative to the binary/script path, where *MDiocre* will look
   for Markdown and HTML files and modules. The Markdown files must have the extension
   **\*.md** and the HTML files must have the extension **\*.html**.
   
**build-folder**
   The folder, relative to the binary/script path, where *MDiocre* will output
   the converted and built HTML files.
   
**templates-folder**
   The folder, relative to the binary/script path, where *MDiocre* will look
   for HTML templates.

The *vars* section is where you will put site-wide variables (these may be empty as well). However, these variable
names are special:

**date**
   User-defined, this is used to define the date in the index entries of a module.
   It should be defined in a document-level, and *not* in the configuration files.
   Best practice is to use the ISO-8601 date format (YYYY-MM-DD) so the entries
   may be sorted properly.

**title**
   User-defined, this is used to define the proper title of a document in a module.
   It should be defined in a document-level, and *not* in the configuration files.

**content**
   This should **not** be set anywhere - this is a special variable containing the
   converted content to be put in the template!
   
MDiocre Configuration
~~~~~~~~~~~~~~~~~~~~~~~

This is ``mdiocre.ini``, an example of an *MDiocre configuration*.
Yes, the file should be named that way for it to be read.

.. code-block:: dosini

   [mdiocre]
   detail  = True
   config  = _conf/sample.ini
   logfile = logfile.log

   [build]
   include-html = True
   copy-html = True
   build-exclude = none
   use-prefix = True

   [clean]
   clean-exclude = none

The *mdiocre* section contains settings for the main program, and you may see the following options:

**detail**
   Must be either *True* or *False*. This sets whether or not to display
   valuable logs in the console prompt.
   
**config**
   The *site configuration* to use, relative to the binary/script path.
   
**logfile**
   Log the output to this file, relative to the binary/script path.
   
The *build* section contains settings for the build process, and you may see the following options:

**include-html**
   Must be either *True* or *False*. This sets whether or not to include HTML
   files in the index. If this is *True*, then `copy-html` is also set to *True*.
   
**copy-html**
   Must be either *True* or *False*. This sets whether or not to copy
   HTML files in the source directory to the build directory
   
**use-prefix**
   Must be either *True* or *False*. This sets whether or not to include
   the module name in the index links. For example, if this is set to True,
   an article hyperlink may point to ``module/somepage.html`` instead of
   simply ``somepage.html``. This is userful if your website
   has a `base` tag in the header.
   
**build-exclude**
   This is a comma-separated list of modules to be excluded from
   the build process
   
The *clean* section contains settings for the clean/delete process, and you may see the following options:

**clean-exclude**
   This is a comma-separated list of modules to be excluded from
   the clean process
   
What next?
----------

Now that you have these configuration files, you may adjust them
to your liking.



.. todo:: Finish this section

You will have to create templates and documents. Templates are
html files in a folder, and the documents are stored in a source
folder. The documents are split in what's called "modules", which
are essentially just directories for the site.

draft:

check your configs

setup your templates choose how
your websize will look

setup your source folders and stuff
to make a new module, just make a
folder and include it in the
configs yo
remember to include a
``index.template`` on them if you
want them to be indexed or smth

do this as many times as u can

then hit ``python mdiocre.py build`` or something