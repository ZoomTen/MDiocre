What's new?
===========

3.1 (2020-09-01)
----------------
User
~~~~
* Not much yet.

API
~~~
* The comment-parsing system has been changed in `core`. Instead of going
  through the string directly through `re`, it goes through a parser, which
  really just implements the same functions. This opens up the possibility
  for other formats to be added as an input to MDiocre. ReStructuredText
  support can be added due to this.

* The `MDiocre` class can now take a `parser` or `parser_name` option.
  The `parser` option must be set to a class inheriting `BaseParser`, or
  you can set the `parser_name`. Built-in ones currently include:
  `markdown`, `html`, `rst`. If both `parser` and `parser_name` are
  defined, `parser` takes precedence.

* :meth:`mdiocre.core.MDiocre.sub_func` has been moved to
  :meth:`mdiocre.parsers.sub_func`. The former will be removed in MDiocre
  3.2.
