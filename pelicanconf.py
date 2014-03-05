#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Josh Izaac'
SITENAME = u'+josh'
SITESUBTITLE = u'iza.ac'
SITEURL = 'http://iza.ac'
EMAIL_ADDR = 'josh at iza dot ac'

TIMEZONE = 'Australia/Perth'

DEFAULT_LANG = u'en'

OUTPUT_PATH = 'output' #os.path.abspath('../../trunk')

IGNORE_FILES = ['plugins/*','pelican-themes/*']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINK_MENU_NAME = 'More'
LINKS =  (  ('Publications','publications'),
            ('cv', 'cv'),
            ('Archive', 'archives'),)

MENUITEMS = (
    # ('About', '/about'),
    ('Blog', '/blog'),
)

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

# Social widget
SOCIAL = (('Facebook', 'http://facebook.com/thispage'),
          ('Google-Plus', 'http://plus.google.com/+JoshIzaac'),
          ('GitHub', 'http://github.com/josh146'),
          ('envelope-o', 'mailto:josh@iza.ac'),)

STATIC_PATHS = ['images', 'extras/CNAME']
EXTRA_PATH_METADATA = {'extras/CNAME': {'path': 'CNAME'},}

DEFAULT_PAGINATION = 10

COPYRIGHT = 'Copyright Josh Izaac, 2014'

# Formatting for dates

DEFAULT_DATE_FORMAT = ('%a %d %B %Y')

# Formatting for urls
PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}.html"

ARTICLE_URL = "posts/{date:%Y}/{date:%m}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%m}/{slug}/index.html"

CATEGORY_URL = "category/{slug}"
CATEGORY_SAVE_AS = "category/{slug}/index.html"

TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATH = 'plugins'
PLUGINS = ['render_math', 'neighbors', 'summary','googleplus_comments',
            'pelican_youtube','better_figures_and_images','pelican-bibtex']

GPLUS_COMMENTS = True
PUBLICATIONS_SRC = 'content/extras/pubs.bib'

# THEME = "pelican-themes/gum"
# THEME = "pelican-themes/notmyidea-cms"
# THEME = "pelican-themes/pelican-bootstrap3"
# THEME = "pelican-themes/simple-bootstrap"
# THEME = "pelican-themes/tuxlite_zf"
THEME = "pelican-themes/BT3-Flat"
# THEME = "pelican-themes/crowsfoot"

BOOTSTRAP_THEME = 'united'

if THEME == "pelican-themes/BT3-Flat":
    HOME_PAGE_STYLE = 'half'
    HEADER_SIZE = HOME_PAGE_STYLE+"-screen"
    BG_IMAGE = "images/cover.JPG"
    BG_IMAGE_TYPE = HOME_PAGE_STYLE+"screen-img"
    # BG_IMAGE_CAPTION = 

    PERSONAL_INFO = """
    I am a PhD student in the 
    <a href=http://www.physics.uwa.edu.au/research/quantum-dynamics-computation>Quantum Dynamics and Computation</a>
    research group at the <a href=http://uwa.edu.au>University of Western Australia</a>, currently researching continuous-time
    quantum walks and potential biological models.
    """

    # PERSONAL_PHOTO = "https://fbcdn-sphotos-g-a.akamaihd.net/hphotos-ak-frc3/t1/q71/s720x720/1476196_10151782687192131_150386508_n.jpg"

    WORK_DESCRIPTION = """
    Testing Travis deployment
    """
    WORK_PUBLICATIONS = True

    WORK_LIST = [['link',
                'http://www.oneperth.com.au/wp-content/uploads/2010/08/UWA.jpg',
                'PhD Student',
                'Student',
                'http://uwa.edu.au']]

    POST_LIMIT = 5
    # TEMPLATE_PAGES = {  'templates/blog.html': 'blog.html'}
    DIRECT_TEMPLATES = ('index', 'archives','publications', 'blog')