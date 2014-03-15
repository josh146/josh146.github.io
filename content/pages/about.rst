About
#####################
:subtitle: why would this need a subtitle
:author: Josh Izaac
:excerpt: This is an excerpt of my post.
:date: 2012-10-15 23:06
:tags: helloworld, blog, first

Introduction
------------

Hi!

This is my first rst post!

And this is a link to a `page <iza.ac>`_

This is a test list:

* option 1
* option 2

This is another unordered list:

- option1
- option 2
- option3
  
This is an ordered list:

#. Option number 1
#. option number 2
#. This should be formatted as option number 3

------------

blah blah blah

Testing some ReST features
----------------------------


what
    Definition lists associate a term with
    a definition.

how
    The term is a one-line phrase, and the
    definition is one or more paragraphs or
    body elements, indented relative to the
    term. Blank lines are not allowed
    between term and definition.

Autonumbered footnotes are
possible, like using [#]_ and [#]_.

.. [#] This is the first one.
.. [#] This is the second one.

They may be assigned 'autonumber
labels' - for instance,
[#fourth]_ and [#third]_.

.. [#third] a.k.a. third_

.. [#fourth] a.k.a. fourth_ 

This is a simple code example

.. code-block:: python

    import math
    print 'import done'

A Table
----------


+------------+------------+-----------+
| Header 1   | Header 2   | Header 3  |
+============+============+===========+
| body row 1 | column 2   | column 3  |
+------------+------------+-----------+
| body row 2 | Cells may span columns.|
+------------+------------+-----------+
| body row 3 | Cells may  | - Cells   |
+------------+ span rows. | - contain |
| body row 4 |            | - blocks. |
+------------+------------+-----------+

Embedding a PDF
----------------

Embedding a PDF:

.. embedly-card:: http://iza.ac/pdf/cv.pdf
    :card-chrome: 0

.. gmaps:: The queens larder, london
    :mode: place
