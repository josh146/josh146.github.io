#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

#~~~~~~~~~~~~~~~~
## Main Settings
#~~~~~~~~~~~~~~~~

AUTHOR = u'Josh Izaac'
SITENAME = u'+josh'
SITESUBTITLE = u'iza.ac'
SITEURL = 'http://iza.ac'
EMAIL_ADDR = 'josh at iza dot ac'
COPYRIGHT = 'Copyright Josh Izaac, 2014'

DISQUS_SITENAME = 'izaac'
SWIFTYPE = 'LPcmywgYs12nMZT1EFp7'

TIMEZONE = 'Australia/Perth'

DEFAULT_LANG = u'en'

OUTPUT_PATH = 'output'  # os.path.abspath('../../trunk')

IGNORE_FILES = ['plugins/*', 'pelican-themes/*']

DEFAULT_PAGINATION = 10

# Formatting for dates
DEFAULT_DATE_FORMAT = ('%a %d %B %Y')
DEFAULT_DATE = 'fs'

USE_FOLDER_AS_CATEGORY = True
AUTHORS_SAVE_AS = None

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

#~~~~~~~~~~~~~~~~
# Feed settings
#~~~~~~~~~~~~~~~~
FEED_DOMAIN = SITEURL

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

FEED_RSS = 'rss.xml'
CATEGORY_FEED_RSS = '%s/rss.xml'

#~~~~~~~~~~~~~~~~
# Navbar settings
#~~~~~~~~~~~~~~~~

LINK_MENU_NAME = 'More'

try:
    if RELATIVE_URLS:
        LINKS = (('Publications', 'http://127.0.0.1:8000/publications'),
                 ('cv', 'http://127.0.0.1:8000/pdf/cv.pdf'),
                 ('Archive', 'http://127.0.0.1:8000/archives'),
                 ('Feed', 'http://127.0.0.1:8000/rss.xml'),
            	 ('Search', 'http://127.0.0.1:8000/search'),)
except:
    LINKS = (('Publications', SITEURL+'/publications'),
             ('cv', SITEURL+'/pdf/cv.pdf'),
             ('Archive', SITEURL+'/archives'),
             ('Feed', SITEURL+'/rss.xml'),
             ('Search', SITEURL+'/search'),)

MENUITEMS = (
    # ('About', '/about'),
    ('Blog', '/blog'),
)

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

GITHUB_URL = 'http://github.com/josh146'

# Social widget
SOCIAL = (('Facebook', 'http://facebook.com/thispage'),
          ('Google-Plus', 'http://plus.google.com/+JoshIzaac'),
          ('GitHub', 'http://github.com/josh146'),
          ('envelope-o', 'mailto:josh@iza.ac'),
          ('rss', SITEURL+'/rss.xml'),)

# SOCIALFOOTER = (('GitHub', 'http://github.com/josh146'),)

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

CATEGORY_URL = "category/{slug}"
CATEGORY_SAVE_AS = "category/{slug}/index.html"

TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"


#~~~~~~~~~~~~~~~~
# Plugins
#~~~~~~~~~~~~~~~~

PLUGIN_PATH = 'plugins'
PLUGINS = ['render_math',
           'neighbors',
           'summary',
           'googleplus_comments',
           'pelican_youtube',
           'better_figures_and_images',
           'pelican-bibtex',
           'minify']

GPLUS_COMMENTS = False
RESPONSIVE_IMAGES = True
RESPONSIVE_IMAGES = True
FIGURE_NUMBERS = True

#~~~~~~~~~~~~~~~~
# Pelican-Bibtex
#~~~~~~~~~~~~~~~~

PUBLICATIONS_SRC = 'content/extras/pubs.bib'

#~~~~~~~~~~~~~~~~
# Theme settings
#~~~~~~~~~~~~~~~~

# THEME = "pelican-themes/gum"
# THEME = "pelican-themes/notmyidea-cms"
# THEME = "pelican-themes/pelican-bootstrap3"
# THEME = "pelican-themes/simple-bootstrap"
# THEME = "pelican-themes/tuxlite_zf"
THEME = "pelican-themes/BT3-Flat"
# THEME = "pelican-themes/elegant"
# THEME = "pelican-themes/crowsfoot"

if THEME == "pelican-themes/elegant":
    personalLinks = ['http://www.physics.uwa.edu.au/research/quantum-dynamics-computation',
                     'http://uwa.edu.au']

    LANDING_PAGE_ABOUT = {}

    LANDING_PAGE_ABOUT['title'] = "An occasional PhD student working with quantum computers"

    
    workLinks = ['http://www.physics.uwa.edu.au/research/quantum-dynamics-computation',
                 'http://uwa.edu.au',
                 'http://www.ivec.org',
                 'http://pyctqw.readthedocs.org']

    WORK_DESCRIPTION = """
    <p style="text-align:left"> 

    I am a PhD student in the <a href={0}>Quantum Dynamics and Computation</a> 
    research group at the <a href={1}>University of Western Australia</a>, 
    currently researching continuous-time quantum walks and potential biological models.<br><br>

    My current research interests mainly lie in the characterisation and applications of quantum walks, 
    with specific focus on quantum simulation of complex biochemical systems such as photosynthesis 
    and electron transport in functional nano-materials.<br><br>

    A major part of my research involves numerical simulation on high performance supercomputing 
    clusters (mainly using the <a href={2}>iVEC</a> supercomputing facility in Western Australia), 
    working mostly with Fortran and Python. In order to streamline my workflow, I developed an efficient 
    parallel framework for simulating continuous-time quantum walks, <a href={3}>pyCTQW</a>, with the 
    source code available on my GitHub page. Other tools I find useful for my work include iPython, 
    matplotlib, the amazingly extendable SublimeText, and of course Mathematica and $\LaTeX{{}}$.<br><br>

    Outside of research, I am also employed as a tutor and lab demonstrator for third year 
    computational physics PHYS3011 at UWA.</p>
    """.format(*workLinks)
    
    LANDING_PAGE_ABOUT['details'] = WORK_DESCRIPTION

    PROJECTS = [{
    'name': 'pyCTQW',
    'url': 'http://pyctqw.readthedocs.org',
    'description': 'Distributed memory continuous-time<br> quantum walk framework'},]


    disqus_identifier = 'izaac'

    DIRECT_TEMPLATES = (('index', 'tags', 'categories','archives', 'search', '404'))
    PLUGINS += ['sitemap', 'extract_toc', 'tipue_search']



if THEME == "pelican-themes/BT3-Flat":
    HOME_PAGE_STYLE = 'half'
    HEADER_SIZE = HOME_PAGE_STYLE+"-screen"
    BG_IMAGE = "images/cover.JPG"
    BG_IMAGE_TYPE = HOME_PAGE_STYLE+"screen-img"
    BG_IMAGE_CAPTION = """
        <a href="#about" class="icon-block scrollTo">
            about&nbsp;<i class="fa fa-chevron-circle-down"></i>
        </a>
        """

    personalLinks = ['http://www.physics.uwa.edu.au/research/quantum-dynamics-computation',
                     'http://uwa.edu.au']

    PERSONAL_INFO = """
    I am a PhD student in the <a href={0}>Quantum Dynamics and Computation</a> 
    research group at the <a href={1}>University of Western Australia</a>, 
    currently researching continuous-time quantum walks and potential biological models.
    """.format(*personalLinks)

    # PERSONAL_INFO_SEC1_TITLE = "Stuff"
    # PERSONAL_INFO_SEC1 = """
    # Some more stuff
    # """

    # PERSONAL_INFO_SEC2_TITLE = "Stuff2"
    # PERSONAL_INFO_SEC2 = """
    # Some more stuff
    # """

    # PERSONAL_INFO_SEC3_TITLE = "Stuff3"
    # PERSONAL_INFO_SEC3 = """
    # Some more stuff
    # """

    # PERSONAL_PHOTO = "https://fbcdn-sphotos-g-a.akamaihd.net/hphotos-ak-frc3/t1/q71/s720x720/1476196_10151782687192131_150386508_n.jpg"

    workLinks = ['http://www.ivec.org',
                 'http://pyctqw.readthedocs.org']

    WORK_DESCRIPTION = """
    <p style="text-align:left"> My current research interests mainly lie in the characterisation and applications of quantum walks, 
    with specific focus on quantum simulation of complex biochemical systems such as photosynthesis 
    and electron transport in functional nano-materials.<br><br>

    A major part of my research involves numerical simulation on high performance supercomputing 
    clusters (mainly using the <a href={0}>iVEC</a> supercomputing facility in Western Australia), 
    working mostly with Fortran and Python. In order to streamline my workflow, I developed an efficient 
    parallel framework for simulating continuous-time quantum walks, <a href={1}>pyCTQW</a>, with the 
    source code available on my GitHub page. Other tools I find useful for my work include iPython, 
    matplotlib, the amazingly extendable SublimeText, and of course Mathematica and $\LaTeX{{}}$.<br><br>

    Outside of research, I am also employed as a tutor and lab demonstrator for third year 
    computational physics PHYS3011 at UWA.</p>
    """.format(*workLinks)

    WORK_PUBLICATIONS = True

    WORK_LIST = [['link',
                'http://pyctqw.readthedocs.org/en/latest/_images/1p_3cayley_graph.png',
                'pyCTQW',
                'Distributed memory continuous-time quantum walk framework',
                'http://pyctqw.readthedocs.org'],
                ['link',
                'images/thesis2.png',
                'Honours Thesis',
                'Continuous-time Quantum Walks:<br> Disorder, Resonance and Interactions',
                'https://dl.dropboxusercontent.com/u/152896/honours_thesis.pdf']]

    SHOW_RECENT_BLOGS = False

    POST_LIMIT = 5
    # TEMPLATE_PAGES = {  'templates/blog.html': 'blog.html'}
    DIRECT_TEMPLATES = ('index', 'archives', 'publications', 'blog', 'tags', 'categories', 'search')
    TAG_SAVE_AS = False
    CATEGORY_SAVE_AS = False
    AUTHOR_SAVE_AS = False


