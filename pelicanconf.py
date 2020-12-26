#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import os

AUTHOR = 'Josh Izaac'
SITENAME = 'josh iza.ac'
SITEURL = 'http://iza.ac'
EMAIL_ADDR = 'josh@iza.ac'
COPYRIGHT = 'Copyright Josh Izaac, 2017'
USER_LOGO_URL = '/images/header.png'

THEME = './themes/voce/'
PATH = 'content'

TIMEZONE = 'Australia/Perth'

DEFAULT_LANG = 'en'
DEFAULT_DATE_FORMAT = "%b %d, %Y"

PLUGIN_PATHS = ["plugins", os.path.join(THEME, "plugins")]
PLUGINS = ['pelican.plugins.embed_tweet', "pelican_youtube"]

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


GOOGLE_ANALYTICS_ID = 'UA-308113-3'
GOOGLE_ANALYTICS_PROP = 'iza.ac'
TAGLINE = "Site Tagline"
MANGLE_EMAILS = True
GLOBAL_KEYWORDS = ("keywords",)

TYPOGRIFY = True
TYPOGRIFY_DASHES = 'oldschool'

#~~~~~~~~~~~~~~~~
# Navbar settings
#~~~~~~~~~~~~~~~~


SOCIAL = (
    ("Twitter", "https://twitter.com/3rdquantization"),
	('LinkedIn', 'https://linkedin.com/pub/josh-izaac/104/9bb/6a2'),
	('GitHub', 'http://github.com/josh146'),
	('Google Scholar', 'https://scholar.google.com/citations?user=pEj09c4AAAAJ'),
	('Email', 'mailto:josh@iza.ac'),
    ("Feed", "https://siteurl.com/feeds/all.atom.xml"),
)

LINKS = (
    ("About", "/"),
	("CV", "/cv"),
	("posts", "/posts"),
)

DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = [".git"]

DEFAULT_PAGINATION = 5
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
SUMMARY_MAX_LENGTH = 50


#~~~~~~~~~~~~~~~~
# Paths and URLS
#~~~~~~~~~~~~~~~~

STATIC_PATHS = ['images', 'extras/CNAME', 'extras/htaccess', 'pdf']
EXTRA_PATH_METADATA = {'extras/CNAME': {'path': 'CNAME'},
                        'extras/htaccess': {'path': '.htaccess'},}

# Formatting for urls
PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}.html"

ARTICLE_URL = "posts/{date:%Y}/{date:%m}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%m}/{slug}/index.html"
INDEX_SAVE_AS = "posts/index.html"

CATEGORY_URL = "category/{slug}"
CATEGORY_SAVE_AS = "category/{slug}/index.html"

TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"

TAGS_URL = 'tags.html'
ARCHIVES_URL = 'archives.html'

