Interfaces
==========

**Interfaces** are what makes MDiocre usable by the common user, by stringing
together its various core functionalities into something that can process
source files into publishable web pages. Internally, these are referred as
**wizards**, and is what MDiocre calls "interfaces", graphical or otherwise.

Command line
------------

The main operation of command line version of MDiocre needs 2 arguments, namely
the source directory and the destination (build) directory.

The app will copy each file in the source directory recursively and copy them
to the respective folders in the build directory, making them when necessary.
In the case of ``.md`` files, it will parse them. If it finds a
``mdiocre-template`` definition linking to a valid file, it will convert the
file into a usable HTML page.

Consider a folder named `pages` which are full of pages and misc. files that
are targeted to be copied and published, and that the build folder be named
`publish`. MDiocre would be invoked as:

.. code-block::

   python mdiocre.py pages publish

When run, a detailed output of what MDiocre is doing will pop up quickly in
the command line window. If this is undesired, the CLI also offers a "quiet"
option, as `-q` or `--quiet`:

.. code-block::

   python mdiocre.py -q pages publish

.. code
