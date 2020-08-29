What to Know
============

What changed in 3.0?
--------------------

* The project **no longer requires Pandoc**, as the focus is Markdown-only for now. reStructuredText will be put under later consideration.

* The comment syntax has changed:
	* It isn't as space-sensitive as before.
	* It has a standardized prefix: The ``:`` character. So...
		* ``<!--var:something-->`` is now ``<!--:something-->``
		* ``<!--hello=lemons-->`` is now ``<!--:hello = lemons-->``
		* ``<!--lemons=hello, hello-->`` is now ``<!--:lemons = hello, hello-->``

Why 3.0, or, the History
------------------------

* version 1.0 : Hacked together Bash script: https://gitlab.com/zumid/zumisite-oldtools
* version 2.0 : Interface-focused, monolithic Python script: https://github.com/ZoomTen/MDiocre
* version 3.0 : Neater, compartmentalized Python script (now)

Plans for 3.0
-------------

To have a config-less system that just copies every file one to one. The index
generation will be optional.

The ideal setup
---------------

Markdown + Template = Page

**the Markdown**

.. code-block:: md

	<!--:page-title   = "The Problem with this Shit"-->
	<!--:publish-date = "2020-08-29T23:49:45+07:00" -->
	
	# <!--:page-title-->
	
	Published on <!--:publish-date-->
	
	Lorem ipsum dolor sit amet...	
	
**the Template**

.. code-block:: html

	<html>
		<head>
			<title><!--:page-title--> - Zumi's Realm</title>
		</head>
		<body>
			<div class="main">
			<!--:content-->
			</div>
		</body>
	</html>

**the Page**

.. code-block:: html

	<html>
		<head>
			<title>The Problem with this Shit - Zumi's Realm</title>
		</head>
		<body>
			<div class="main">
				<h1>The Problem with this Shit</h1>
	
				<p>Published on 2020-08-29T23:49:45+07:00</p>
				
				<p>Lorem ipsum dolor sit amet...</p>
			</div>
		</body>
	</html>
