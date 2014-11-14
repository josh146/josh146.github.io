##############
Google Embed
##############
:subtitle: Pelican plugin
:date: 2014-03-23 22:27
:tags: python, pelican
:category: Technology
:author: Josh Izaac

.. |br| raw:: html

    <br />

In my previous post, when discussing `Embedly-cards <{filename}embedly-cards.rst>`_, I enthusiastically exclaimed

    The produced embeddable cards support almost *any* source - articles, Amazon products, YouTube videos, PDFs, forum posts, etc (even Google+ albums!).

Well, turns out I was getting a bit ahead of myself. After playing around with it a bit more, I found it doesn't deal so well with Google Maps and Places - useful embeddable objects if you are blogging whilst travelling, for example. So, after checking if anything better exists for Google Maps integration (and not finding anything whatsoever), I decided 'why not!'.

So, here is the result of an hour of procrastination: the `Google-Embed`_ Pelican_ plugin (disclaimer: there are more than likely a couple of bugs here and there - let me know if you come across any).

.. _Google-Embed: https://github.com/josh146/google_embed/
.. _Pelican: http://getpelican.com

To install it, simply run

.. code-block:: bash
    
    $ pip install google-embed

and add it to your ``pelicanconf.py`` file (for more configuration options, see the readme over at `GitHub <https://github.com/josh146/google_embed/>`__).


Examples
==========

|br|

Embedding Google+ posts
--------------------------

.. code-block:: rest

    .. gplus:: https://plus.google.com/113507009175485747967/posts/LoDoq8ieTp8

.. gplus:: https://plus.google.com/113507009175485747967/posts/LoDoq8ieTp8

|br|

Embed Google Maps
---------------------

**In place mode:**

.. code-block:: rest

    .. gmaps:: Tower of London
        :mode: place


.. gmaps:: Tower of London
    :mode: place


**In search mode:**

.. code-block:: rest

    .. gmaps:: Mexican restaurants near Westminster Abbey
        :mode: search

.. gmaps:: Mexican restaurants near Westminster Abbey
    :mode: search

|br|

Embed Directions
------------------

.. code-block:: rest

    .. directions::
        :mode: transit
        :origin: Tower of London
        :destination: Westminster Abbey

.. directions::
    :mode: transit
    :origin: Tower of London
    :destination: Westminster Abbey

|br|

Embed Google Map as an Image
-----------------------------

.. code-block:: rest

    .. static-map:: The queens larder
        :markers: color:blue label:A The+British+Museum & color:red label:B The+queens+larder
        :zoom: 15
        
.. static-map:: The queens larder
    :markers: color:blue label:A The+British+Museum & color:red label:B The+queens+larder
    :zoom: 15

|br|

Embed Streetview as an Image
------------------------------

.. code-block:: rest

    .. streetview:: Paragon, Orchard Rd

.. streetview:: Paragon, Orchard Rd
