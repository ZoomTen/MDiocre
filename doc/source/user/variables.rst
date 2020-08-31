Variables
=========

**Variables** are simply HTML comments formatted
in a particular way. The first character after the comment markup should
be a colon (:), both for setting and getting variables.

There not many restrictions for variable names. It can have funky letters,
spaces, etc. as long as there isn't a `=`, since that is used for determining
where the value starts

Setting variables
-----------------

Variables are defined simply in the form of `identifier = value`, where the
`identifier` is the variable's name, and the `value` can be a concatenation or
a simple value define.

Basic
~~~~~
Directly assign a value to a variable. These can be either:

   * **A string.** They are marked with quotes around the text, and the
     beginning quotation mark must match the end quotation mark. The backslash
     (\) functions as an escape character, so if you want to use a backslash,
     put two. Computers are hard... so if you plan on using a comma (,) make sure
     that they are escaped with backslash (\) !
     
     .. code-block::
        
        <!--: String = "my string" -->
   
   * **A math equation.** Addition, subtraction, multiplication, division only,
     but no parentheses!
     
     .. code-block::
        
        <!--: Math = 3 * 7 + 1 - 1 -->

Concatenation
~~~~~~~~~~~~~
String together two or more variables and strings. Each entry is appended one
after another without spaces in between, so if a space between is desired, it
would have to be appended as a string.

.. code-block::

   <!--: String2 = String, String -->

would make `String2` equal "my stringmy string", while:

.. code-block::

   <!--: String2 = String, " ", String -->

would make `String2` equal "my string my string".

Getting variables
-----------------
It is as simple as simply saying the name of the variable (and nothing else)
within the comment.

Any instance of this:

.. code-block::

   <!--: String -->

Would be replace with whatever is stored in `String`, that is simply the phrase
"my string".

Example
-------
Say you want a variable named `copyright` that simply contains the copyright
text of your page or site. You set it by saying:

.. code-block:: html

   <!--: copyright = "2020 Zumi" -->

Note how the quotes go around the thing you want to set it to, because it marks
the entire thing as a string.

In case you want another variable containing the full copyright string, you can
use concatenation:

.. code-block:: html

   <!--: copyright text = copyright, ". All rights reserved." -->

This tells it to store a variable named `copyright text` that takes the text
in `copyright` and appends the string `". All rights reserved."` right after
it, without any space before it.

If you write the `copyright` variable assignment as ``<!--: copyright = 2020 Zumi -->``
it will assume the ``copyright`` variable must be equal to the value in the
variable ``2020 Zumi``, and that's not very ideal..
