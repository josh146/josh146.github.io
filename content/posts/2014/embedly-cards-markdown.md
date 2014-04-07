Title: Embedly Cards v0.2 - Markdown support
Subtitle: now with added Markdownly goodness
Date: 2014-04-07 12:23
Tags: python, pelican
Category: Technology
Author: Josh Izaac
Timezone: +0800

I've just updated the embedly-cards [Pelican](http://getpelican.com) plugin to version 0.2, adding markdown support; the new version can be downloaded from [GitHub](http://github.com/josh146/embedly_cards) or [PyPi](https://pypi.python.org/pypi/embedly_cards) (if you have already installed it via `pip`, it can be upgraded via `pip install embedly-cards --upgrade`).

Pelican tends to favour reStructuredText extensions in it's configuration (I guess due to the 'pythonic' nature of reStructuredText), and so setting up the embedly-cards markdown extension is slightly more convulated (but still pretty simple, at only 2 lines!). Simply add the following to your `pelicanconf.py` file:

	:::python
	from embedly_cards import EmbedlyCardExtension
	MD_EXTENSIONS = ['codehilite(css_class=highlight)',
	                 'extra',
	                 EmbedlyCardExtension()]

As far as I can tell, defining `MD_EXTENSIONS` overwrites the default Pelican value, so be sure to include `'codehilite(css_class=highlight)'` and `'extra'` along with other markdown extensions you are currently using (otherwise you'll lose code highlighting support).

If you would like to use both the markdown *and* the ReST extensions, simply add `'embedly_cards'` to the `PLUGINS` list *in addition* to defining `MD_EXTENSIONS`.

##Usage

Once installed, to embed content in markdown files, simply use

	[!embedlycard](url)

where `url` is the url of the website containing the embeddable data. Similarly to the ReST extension, you can optionally pass the `chrome` parameter to force the embedded card to retain its border:

	[!embedlycard?chrome=1](url)

(leaving off this parameter is equivalent to passing `chrome=0`; i.e. the default will be to try and remove the border *if supported*).

##Examples

###Embedding an StackOverflow post:

	[!embedlycard](http://physics.stackexchange.com/questions/5265/cooling-a-cup-of-coffee-with-help-of-a-spoon)

[!embedlycard](http://physics.stackexchange.com/questions/5265/cooling-a-cup-of-coffee-with-help-of-a-spoon)


###Embedding a YouTube video *with* card border:

	[!embedlycard?chrome=1](https://www.youtube.com/watch?v=ZlfIVEy_YOA)

[!embedlycard?chrome=1](https://www.youtube.com/watch?v=ZlfIVEy_YOA)


###Embedding a YouTube video *without* card border:

	[!embedlycard](https://www.youtube.com/watch?v=ZlfIVEy_YOA)

[!embedlycard](https://www.youtube.com/watch?v=ZlfIVEy_YOA)

