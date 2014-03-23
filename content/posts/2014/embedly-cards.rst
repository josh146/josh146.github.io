Embedly Cards
##############
:subtitle: Pelican plugin
:date: 2014-03-23 15:03
:timezone: +0800
:tags: python, pelican
:category: Technology
:author: Josh Izaac

This blog is built using `Pelican <http://getpelican.com>`__, an awesome static blog generator written in Python, requiring no database or server-side scripting - in fact, all content is generated from simple reStructuredText or Markdown files (including this page, if you look at the source). Compared to a CMS like Wordpress, this results in increased speed, the ability to use static "web-hosts" (like `GitHub <http://github.com>`__ or `Dropbox <http://dropbox.com>`__ - not strictly what they were designed for, especially Dropbox, but it works - and they're free!), and, depending on your point of view, easier content management/backup. Of course, you lose certain features, like online or mobile posting, but with DroidEdit on Android now supporting Git, online editing of files on GitHub, and the ability to build your site automatically on git pushes using continuous integration sites such as `Travis CI <http://travis-ci.com>`__ (see `this tutorial <http://zonca.github.io/2013/09/automatically-build-pelican-and-publish-to-github-pages.html>`__), it's very nearly there.

However, as reStructuredText is not designed for dynamic web content, embedding external content is difficult - this is alleviated somewhat by `Pelican plugins <https://github.com/getpelican/pelican-plugins>`__ such as Pelican-Youtube_ and Pelican-Vimeo_, but this approach requires the continual development of similar plugins for further types of content. On the other end of the spectrum, there is html_rst_directive_; but this requires that

1. the external site provides easy-to-access HTML for embeddable content
2. and if it does, you will probably need to be on the desktop site, excluding phone apps/sites/blogging-on-the-go.
   
Another approach is a Python plugin using the oEmbed_ standard, allowing the embeddable HTML to be recieved and inserted on blog generation. I played around with two such plugins, PyEmbed_ and `sphinxcontrib.embedly`_, the latter of which uses `Embed.ly`_ oEmbed central repository. Whilst both are nice solutions, I still wasn't able to embed all the sources I was hoping to.

However, I noticed that `Embed.ly`_ has a new poduct called `Embed.ly Cards <http://embed.ly/cards>`__:

	Cards provide a clean, responsive, and shareable card for any content on the web.
	Use them to make your posts easier to share and repost across the web. You can also include rich content from other sites in your own posts with Cards. 

The produced embeddable cards support almost *any* source - articles, Amazon products, YouTube videos, PDFs, forum posts, etc (even Google+ albums!). What's more, they look really *good*, with a subtle coloured left border giving a 'quote' effect, rich content, and a short excerpt if available - this is the sort of standardised formatting I was looking for. They can even be used for your own content, providing a 'richer' linking experience between blog posts!

Embedly-cards plugin
-----------------------

So I wrote a small Pelican plugin allowing Embed.ly cards to be easily inserted in posts; the source code is available on `Github <https://github.com/josh146/embedly_cards>`__, and it can be installed using ``pip``:

.. code-block:: bash

	$ pip install embedly-cards		

Check out the `Github repo <https://github.com/josh146/embedly_cards>`__ for more information. Below are some quick examples.

Examples
------------

Embedding a Google+ album using the public share key:

.. code-block:: rest

	.. embedly-card:: https://plus.google.com/photos/107452285898786120113/albums/5962126455360751089?authkey=CKv687-PodGg0gE

.. embedly-card:: https://plus.google.com/photos/107452285898786120113/albums/5962126455360751089?authkey=CKv687-PodGg0gE

Embedding a photo:

.. code-block:: rest

	.. embedly-card:: https://lh5.googleusercontent.com/n7iY8f5n8qJcZraH3bvRJdpdZiYlsT_wU5ZZznpKIxHU=w1351-h901-no

.. embedly-card:: https://lh5.googleusercontent.com/n7iY8f5n8qJcZraH3bvRJdpdZiYlsT_wU5ZZznpKIxHU=w1351-h901-no

Embedding an StackOverflow post:

.. code-block:: rest

	.. embedly-card:: http://physics.stackexchange.com/questions/5265/cooling-a-cup-of-coffee-with-help-of-a-spoon

.. embedly-card:: http://physics.stackexchange.com/questions/5265/cooling-a-cup-of-coffee-with-help-of-a-spoon

Embedding a YouTube video *with card border*:

.. code-block:: rest

	.. embedly-card:: https://www.youtube.com/watch?v=ZlfIVEy_YOA
		:card-chrome: 1

.. embedly-card:: https://www.youtube.com/watch?v=ZlfIVEy_YOA
	:card-chrome: 1

Embedding a YouTube video *without card border*:

.. code-block:: rest

	.. embedly-card:: https://www.youtube.com/watch?v=ZlfIVEy_YOA

.. embedly-card:: https://www.youtube.com/watch?v=ZlfIVEy_YOA

An embedded PDF:

.. code-block:: rest

	.. embedly-card:: https://media.readthedocs.org/pdf/pelican/latest/pelican.pdf

.. embedly-card:: https://media.readthedocs.org/pdf/pelican/latest/pelican.pdf


.. _Pelican-Youtube: https://github.com/kura/pelican_youtube
.. _Pelican-Vimeo: https://github.com/kura/pelican_vimeo
.. _html_rst_directive: https://github.com/getpelican/pelican-plugins/tree/master/html_rst_directive

.. _PyEmbed: http://pyembed.github.io/
.. _oEmbed: http://oembed.com/
.. _Embed.ly: http://embed.ly/
.. _sphinxcontrib.embedly: https://jezdez.com/2014/01/26/embedding-external-content-in-rst/