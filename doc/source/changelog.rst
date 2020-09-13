What's new?
===========

3.1 (2020-09-13)
----------------
User
~~~~
* Introducing a simple Tk GUI for MDiocre (`mdiocre_gui.py`). Its features
  currently match that of the CLI version (`mdiocre.py`), but individual file
  conversion and string conversion is planned.

* Added sample scripts that use the MDiocre API
    * RSS feed generator (`samples/make_feed.py`)
    * Index page generator, with pagination (`samples/make_index.py`)
    * Tags page generator (`samples/make_tags.py`)

API
~~~
* The comment-parsing system has been changed in `core`. Instead of going
  through the string directly through `re`, it goes through a parser, which
  really just implements the same functions. This opens up the possibility
  for other formats to be added as an input to MDiocre. ReStructuredText
  support can be added due to this.

* The `Wizard` can now take a `callback` function. The callback function is
  run after each file is processed, and passes a dict containing the original
  file name, the converted file name, as well as the root directory.

* The `MDiocre` class can now take a `parser` or `parser_name` option.
  The `parser` option must be set to a class inheriting `BaseParser`, or
  you can set the `parser_name`. Built-in ones currently include:
  `markdown`, `html`, `rst`. If both `parser` and `parser_name` are
  defined, `parser` takes precedence.

* :meth:`mdiocre.core.MDiocre.sub_func` has been moved to
  :meth:`mdiocre.parsers.sub_func`. The former will be removed in MDiocre
  3.2.

3.0 (2020-08-31)
----------------

All-new rewrite of MDiocre, with the aim to "modularize" it and keep it easy-to-use.
