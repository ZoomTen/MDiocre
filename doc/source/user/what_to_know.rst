What to Know
============

What's a MDiocre?
-----------------

**MDiocre** is a simple static website generator that takes Markdown-formatted files, as well as a template and inserts whatever the Markdown content is into the template. It does this by using specially-formatted HTML comments which can set and get variables from and within the content, and to the template.

Why should I use it?
--------------------

Well... if you're looking for something sophisticated, don't - you might be better off with `Jekyll <https://jekyllrb.com/>`_ or `Hugo <https://gohugo.io/>`_. Or anything from `here <https://www.staticgen.com>`_.

What changed in 3.0?
--------------------

* The project **no longer requires Pandoc**, which is kind of overkill for a project that's just going to use
  Markdown anyway.

* It is overall **lighter** than version 2.0, and less "monolithic". Every file is simply copied / converted over from the source directory to the build directory, no need for that "having to process images and HTML separately" bs.

* **No more fussing around** with configuration files (what do you mean I must have 2 config files?!). Templates are evaluated on a
  per-file basis. And yeah, that means throwing away that entire concept of
  "submodules", lol.

* To add to the previous point, it has been substituted with the concept of a **per-file template linking**. The downside is of course, more chores to be done when changing folder structures. But it can give you more control rather than having to fight the configs.

* **API-minded**, has string-based functions that expose the core functionality of MDiocre.

* The **comment syntax has changed**:
	* It isn't as space-sensitive as before.
	* It has a standardized prefix: The ``:`` character. So...
		* ``<!--var:something-->`` is now ``<!--:something-->``
		* ``<!--hello=lemons-->`` is now ``<!--:hello = lemons-->``
		* ``<!--lemons=hello, hello-->`` is now ``<!--:lemons = hello, hello-->``

* You can **perform basic math** and assign it to a variable. Something like: ``<!--:math = 3 * 9 + 1 / 5-->``

* **No limitations** on variable names! (theoretically...)
  So instead of ``lame_variable_name`` you can have names that look like... well,
  normal names! Like ``aWeSoMe VaRiabLe nAmE``! And yes, that means ``<!--:aWeSoMe = 4 * 7 + 2-->`` or ``<!--:aWeSoMe-->``

tl;dr: It's way simpler now :)

Why 3.0, or, the History
------------------------

MDiocre was originally written in 2018 to generate a newer iteration of `my website <https://zumi.neocities.org>`_. It was initially several bash scripts that combined various tools with `pandoc` to create an easy workflow for me to blog, that can even be used on the go.

I then rewrote it in Python with the intent of having an easier, more "general" way of makin static websites. It turned out to be rather cumbersome with the configuration files and the concept of "submodules" and such. Nevertheless, this is what I used to maintain my website for some time. Another flaw with this iteration is that it assumes a ToC-like index in a particular format, and it could not be customized. The no-index pages had to be explicitly stated in the site configs.

I decided it would be best to start off from scratch and rethink the design of MDiocre. I intend for this version to be a lot simpler to deal with.

In summary, we now have 3 iterations of MDiocre:
   * **version 1.0** : Hacked together Bash script: https://gitlab.com/zumid/zumisite-oldtools
   * **version 2.0** : Interface-focused, monolithic Python script: https://github.com/ZoomTen/MDiocre
   * **version 3.0** : Neater Python script (now)

Plans for 3.1
-------------
Hacking in reStructured Text as well as modular index page generation.
