#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import os

AUTHOR = "Josh Izaac"
SITENAME = "josh iza.ac"
SITEURL = "http://iza.ac"
EMAIL_ADDR = "josh@iza.ac"
COPYRIGHT = "Copyright Josh Izaac, 2017"
USER_LOGO_URL = "/images/header.png"
LOGO = "https://iza.ac/images/header.png"

THEME = "./themes/voce/"
PATH = "content"

TIMEZONE = "Australia/Perth"

DEFAULT_LANG = "en"
DEFAULT_DATE_FORMAT = "%b %d, %Y"

PLUGIN_PATHS = ["plugins", os.path.join(THEME, "plugins")]
PLUGINS = [
    "pelican.plugins.embed_tweet",
    "pelican_youtube",
    "pelican.plugins.render_math",
    "pelican.plugins.simple_footnotes",
    "cookbook"
    # "pelican.plugins.seo"
]

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_RSS = "feeds/rss.xml"
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

USE_FOLDER_AS_CATEGORY = True


GOOGLE_ANALYTICS_ID = "UA-308113-3"
GOOGLE_ANALYTICS_PROP = "iza.ac"
TAGLINE = "Site Tagline"
MANGLE_EMAILS = True
GLOBAL_KEYWORDS = ("keywords",)

TYPOGRIFY = True
TYPOGRIFY_DASHES = "oldschool"

MATHJAX_CONF = {"auto_insert": True}

SEO_REPORT = False
SEO_ENHANCER = True
SEO_ENHANCER_OPEN_GRAPH = True

# ~~~~~~~~~~~~~~~~
# Navbar settings
# ~~~~~~~~~~~~~~~~


SOCIAL = (
    ("Google Scholar", "https://scholar.google.com/citations?user=pEj09c4AAAAJ"),
    ("GitHub", "http://github.com/josh146"),
    ("LinkedIn", "https://linkedin.com/pub/josh-izaac/104/9bb/6a2"),
    ("Email", "mailto:josh@iza.ac"),
    ("Feed", "/feeds/rss.xml"),
)

LINKS = (
    ("Home", "/"),
    ("About", "/about"),
    ("CV", "/cv"),
    ("recipes", "/recipes"),
    ("posts", "/posts")
)

DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = [".git"]

DEFAULT_PAGINATION = 5
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
SUMMARY_MAX_LENGTH = 50


# ~~~~~~~~~~~~~~~~
# Paths and URLS
# ~~~~~~~~~~~~~~~~

STATIC_PATHS = ["images", "extras/CNAME", "pdf"]
EXTRA_PATH_METADATA = {
    "extras/CNAME": {"path": "CNAME"},
    "extras/htaccess": {"path": ".htaccess"},
}

# Formatting for urls
PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}.html"

RECIPE_URL = 'recipes/{slug}/'
RECIPE_SAVE_AS = 'recipes/{slug}/index.html'

ARTICLE_URL = "posts/{date:%Y}/{date:%m}/{slug}/"
ARTICLE_EXCLUDES = ['recipes']
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%m}/{slug}/index.html"
INDEX_SAVE_AS = "posts/index.html"

CATEGORY_URL = "category/{slug}"
CATEGORY_SAVE_AS = "category/{slug}/index.html"

TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"

TAGS_URL = "tags.html"
ARCHIVES_URL = "archives.html"
