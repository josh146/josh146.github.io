#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os, sys

#~~~~~~~~~~~~~~~~
## Main Settings
#~~~~~~~~~~~~~~~~

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

AUTHOR = u'Josh Izaac'
SITENAME = u'+josh'
SITESUBTITLE = u'iza.ac'
SITEURL = 'http://iza.ac'
EMAIL_ADDR = 'josh at iza dot ac'
COPYRIGHT = 'Copyright Josh Izaac, 2017'

DISQUS_SITENAME = 'izaac'
SWIFTYPE = 'LPcmywgYs12nMZT1EFp7'
GOOGLE_ANALYTICS = 'UA-308113-3'
GOOGLE_ANALYTICS_DOMAIN = 'iza.ac'

TIMEZONE = 'Australia/Perth'

DEFAULT_LANG = u'en'

OUTPUT_PATH = 'output'  # os.path.abspath('../../trunk')

IGNORE_FILES = ['plugins/*', 'pelican-themes/*']


# Formatting for dates
DEFAULT_DATE_FORMAT = ('%a %d %B %Y')
DEFAULT_DATE = 'fs'

USE_FOLDER_AS_CATEGORY = True
AUTHORS_SAVE_AS = None


SUMMARY_MAX_LENGTH = 100

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
                 ('cv', 'http://127.0.0.1:8000/cv'),
                 ('Archive', 'http://127.0.0.1:8000/archives'),
                 ('Feed', 'http://127.0.0.1:8000/rss.xml'),
                 ('Search', 'http://127.0.0.1:8000/search'),)
except:
    LINKS = (('Publications', SITEURL+'/publications'),
             ('cv', SITEURL+'/cv'),
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
SOCIAL = (# ('Facebook', 'http://facebook.com/thispage'),
          #('Google-Plus', 'http://plus.google.com/+JoshIzaac'),
          ('Linkedin', 'https://au.linkedin.com/pub/josh-izaac/104/9bb/6a2'),
          ('GitHub', 'http://github.com/josh146'),
          ('Instagram', 'http://instagram.com/thispage'),
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

PLUGIN_PATHS = ['plugins']
PLUGINS = ['render_math',
           'neighbors',
           'summary',
           'related_posts',
           'twitter_bootstrap_rst_directives',
           # 'googleplus_comments',
           'pelican_youtube',
           'better_figures_and_images',
           'pelican-bibtex',
           'sitemap',
           'html_rst_directive',
           'google_embed',
           'embedly_cards']

try:
    RELATIVE_URLS
except NameError:
    PLUGINS.append('minify')
else:
    if RELATIVE_URLS is False:
        PLUGINS.append('minify')

sys.path.append('plugins')

from embedly_cards import EmbedlyCardExtension
from BetterPicEmbed import BetterPicEmbedExtension
MD_EXTENSIONS = ['codehilite(css_class=highlight)',
                 'extra',
                 BetterPicEmbedExtension(),
                 EmbedlyCardExtension()]

GMAPS_KEY = 'AIzaSyBX58gSM6y0bd7VqQNPcw9chkmaHhHKUvw'
GPLUS_COMMENTS = False
RESPONSIVE_IMAGES = True
RESPONSIVE_IMAGES = True
FIGURE_NUMBERS = True
SITEMAP = {'format': 'xml'}

#~~~~~~~~~~~~~~~~
# Pelican-Bibtex
#~~~~~~~~~~~~~~~~

PUBLICATIONS_SRC = 'content/extras/pubs.bib'


#~~~~~~~~~~~~~~~~~~~~~~
# Custom Jinja2 Filters
#~~~~~~~~~~~~~~~~~~~~~~
import calendar
import datetime

def month_name(month_number):
    return calendar.month_name[int(float(month_number))]

CURRENT_YEAR = datetime.datetime.now().year

JINJA_FILTERS = {'month_name':month_name}

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


if THEME == "pelican-themes/BT3-Flat":
    PYGMENT_STYLE = 'pygment-iris'
    
    bgimages = ['images/cover.JPG',
                'images/cover2.JPG',
                'images/cover3.JPG',
                'images/cover4.JPG',
                # 'images/cover5.JPG',
                'images/cover6.JPG',
                # 'images/cover7.JPG',
                # 'images/cover8.JPG',
                # 'images/cover9.JPG',
                'images/cover10.JPG',
                'images/cover11.JPG',
                'images/cover12.JPG',
                'images/cover13.JPG',
                'images/cover15.JPG',
                'images/cover16.JPG']
    
    HOME_PAGE_STYLE = 'full'
    HEADER_SIZE = HOME_PAGE_STYLE+"-screen"
    BG_IMAGE = [i.encode('ascii','ignore') for i in bgimages]
    BG_IMAGE_TYPE = HOME_PAGE_STYLE+"screen-img"
    BG_IMAGE_CAPTION = """
        <a href="#about" class="icon-block scrollTo">
            about&nbsp;<i class="fa fa-chevron-circle-down"></i>
        </a>
        """
    BG_BLUR = False

    personalLinks = ['http://xanadu.ai',
                     'http://www.physics.uwa.edu.au/research/quantum-dynamics-computation']

    PERSONAL_INFO = """
    I am a <a href={0}>quantum mechanic</a>, freelance science writer, and software developer, with a PhD in quantum computation
    from the <a href={1}>University of Western Australia</a>.
    """.format(*personalLinks)

    # PERSONAL_INFO_SEC1_TITLE = "Travel"
    # PERSONAL_INFO_SEC1 = """
    # Some more stuff
    # """

    # PERSONAL_INFO_SEC2_TITLE = "Physics"
    # PERSONAL_INFO_SEC2 = """
    # Some more stuff
    # """

    # PERSONAL_INFO_SEC3_TITLE = "Technology"
    # PERSONAL_INFO_SEC3 = """
    # Some more stuff
    # """

    PERSONAL_PHOTO = "images/face5.png"
    
    workLinks = ['http://www.pawsey.org.au/',
                 'http://pyctqw.readthedocs.org',
                 'http://australiangeographic.com.au',
                 'http://www.sciencemag.org/news',
                 'http://xanadu.ai']

    WORK_DESCRIPTION = """
    <p style="text-align:left"> My research interests mainly lie in the characterisation and 
    applications of quantum walks, with specific focus on network analysis algorithms.<br><br>

    A major part of my research involves numerical simulation on high performance supercomputing 
    clusters (mainly using the <a href={0}>Pawsey</a> supercomputing facility in Western Australia), 
    working mostly with Fortran and Python. In order to streamline my workflow, I developed an efficient 
    parallel framework for simulating continuous-time quantum walks, <a href={1}>pyCTQW</a>, with the 
    source code available on my GitHub page. Other tools I find useful for my work include iPython, 
    matplotlib, the amazingly extendable SublimeText, and of course Mathematica and $\LaTeX{{}}$.<br><br>

    Outside of research, I have worked as a tutor, lab demonstrator, and casual lecturer for 
    undergraduate and honours physics units at UWA. I am currently applying my background in quantum
    computation at <a href={4}>Xanadu Quantum Technologies</a> in Toronto, working to develop the software front-end
    to their continuous-variable quantum computating system. 

    I also enjoy science writing and communication - my writing has so far been featured in 
    <a href={2}>Australian Geographic</a> and <a href={3}>Science</a>.</p>
    """.format(*workLinks)

    WORK_PUBLICATIONS = True

    WORK_LIST =[['link',
                 'https://i.imgur.com/9A2tu4W.png',
                 'PhD Thesis',
                 'Continuous-time quantum walks: simulation and application',
                 'http://research-repository.uwa.edu.au/en/publications/continuoustime-quantum-walks-simulation-and-application(2f9e3075-3307-4e56-bf28-f82a17953c1f).html?uwaCustom=thesis'
                ],
                ['link',
                'images/PTwolfram2.png',
                'PT-symmetric Quantum Walks',
                'Software demonstration published on Wolfram Demonstrations Project',
                'http://demonstrations.wolfram.com/PTSymmetricQuantumWalksAndCentralityTestingOnDirectedGraphs/'],
                ['link',
                'images/pyctqw.png',
                'pyCTQW',
                'Distributed memory continuous-time quantum walk framework',
                'http://pyctqw.readthedocs.org'],
                ['link',
                'images/helmets.jpg',
                'People take more risks when wearing helmets',
                'Article published online in Science',
                'http://www.sciencemag.org/news/2016/01/people-take-more-risks-when-wearing-helmets-potentially-negating-safety-benefits-0'],
                ['link',
                'http://d3lp4xedbqa8a5.cloudfront.net/s3/digital-cougar-assets/AusGeo/2015/12/02/59733/Zebra-finches-duet_AustralianGeographic.jpg',
                'Zebra Finch Duets',
                'Article published in Australian Geographic',
                'http://www.australiangeographic.com.au/news/2015/12/zebra-finch-duets'],
                ['link',
                'images/fairywren.jpg',
                'Female fairy-wrens sing for other females',
                'Article published in Australian Geographic',
                'http://www.australiangeographic.com.au/news/2015/10/why-do-female-birds-sing-%281%29'],
                ['link',
                'http://i.imgur.com/AIfAG8M.gif',
                'Testosterone levels affect how much makeup women use',
                'Article published on RedOrbit.com',
                'http://www.redorbit.com/news/health/1113410539/testosterone-levels-affect-how-much-makeup-women-use-110515']
                # ['link',
                # 'images/thesis2.png',
                # 'Honours Thesis',
                # 'Continuous-time Quantum Walks:<br> Disorder, Resonance and Interactions',
                # 'https://dl.dropboxusercontent.com/u/152896/honours_thesis.pdf']
                ]

    CONFERENCES = [
        """J. A. Izaac, X. Zhan, J. Li, P. Xue, P. C. Abbott, X. S. Ma, and J. B. Wang.
        Quantum centrality ranking via quantum walks and its experimental realization.
        Talk presented at <i>17th Asian Quantum Information Science Conference</i>, Singapore. September 2017""",
        """J. A. Izaac, J. B. Wang, P. C. Abbott, and X. S. Ma.
        Quantum centrality testing on directed graphs via PT-symmetric quantum walks.
        Poster presented at <i>PHHQP16: Progress in Quantum Physics with Non-Hermitian Operators</i>, Kyoto, Japan. August 2016""",
        #"""J. A. Izaac and J. B. Wang.
        #Pseudo-Hermitian continuous-time quantum walks on directed graphs.
        #Paper presented at the <i>Complexity of Quantum Information and Computation Workshop</i>, Tsinghua Sanya International Mathematics Forum, Sanya, China. March 2016""",
        """J. A. Izaac and P. J. Metaxas.
        Nanomagnetism with GPUs: simulations of hybrid vortex - domain wall devices.
        Paper presented at the annual <i>iVEC Symposium</i>, Perth, Australia. February 2013"""]

    SCIWRITING = [
            ["People take more risks when wearing helmets, potentially negating safety benefits",
            "http://www.sciencemag.org/news/2016/01/people-take-more-risks-when-wearing-helmets-potentially-negating-safety-benefits-0",
            "Science Magazine",
            "January 2016"],
            ["Zebra Finch Duets",
            "http://www.australiangeographic.com.au/news/2015/12/zebra-finch-duets",
            "Australian Geographic",
            "December 2015"],
            ["Female fairy-wrens sing for other females",
            "http://www.australiangeographic.com.au/news/2015/10/why-do-female-birds-sing-%281%29",
            "Australian Geographic",
            "October 2015"],
            ["Testosterone levels affect how much makeup women use, study finds",
            "http://www.redorbit.com/news/health/1113410539/testosterone-levels-affect-how-much-makeup-women-use-110515",
            "redOrbit",
            "November 2015"]
        ]

    SHOW_RECENT_BLOGS = False

    POST_LIMIT = 5
    TAG_SAVE_AS = False
    CATEGORY_SAVE_AS = False
    AUTHOR_SAVE_AS = False

    DEFAULT_PAGINATION = False

    if DEFAULT_PAGINATION is False:
        DIRECT_TEMPLATES = ('index', 'archives', 'publications', 'cv', 'blog', 'tags', 'categories', 'search')
        TEMPLATE_PAGES = {  'blog.html': 'blog.html'}
    else:
        PAGINATED_DIRECT_TEMPLATES = ('blog-index',)
        PAGINATION_PATTERNS = (
            (1, '{base_name}', '{base_name}/blog/index.html'),
            (2, '{base_name}/blog/{number}/', '{base_name}/blog/{number}/index.html'),
        )
        DIRECT_TEMPLATES = ('index', 'archives', 'publications', 'cv', 'blog-index', 'blog', 'tags', 'categories', 'search')

