#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os, sys

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

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

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
                 ('cv', 'http://127.0.0.1:8000/pdf/cv.pdf'),
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
SOCIAL = (('Facebook', 'http://facebook.com/thispage'),
          #('Google-Plus', 'http://plus.google.com/+JoshIzaac'),
          ('Linkedin', 'https://au.linkedin.com/pub/josh-izaac/104/9bb/6a2'),
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
           'minify',
           'sitemap',
           'html_rst_directive',
           'google_embed',
           'embedly_cards']

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

def month_name(month_number):
    return calendar.month_name[int(month_number)]

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

    HOME_PAGE_STYLE = 'full'
    HEADER_SIZE = HOME_PAGE_STYLE+"-screen"
    BG_IMAGE = "images/cover.JPG"
    BG_IMAGE_TYPE = HOME_PAGE_STYLE+"screen-img"
    BG_IMAGE_CAPTION = """
        <a href="#about" class="icon-block scrollTo">
            about&nbsp;<i class="fa fa-chevron-circle-down"></i>
        </a>
        """
    BG_BLUR = False

    personalLinks = ['http://www.physics.uwa.edu.au/research/quantum-dynamics-computation',
                     'http://uwa.edu.au']

    PERSONAL_INFO = """
    I am a freelance science writer and PhD student in the <a href={0}>Quantum Dynamics and Computation</a> 
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

    #PERSONAL_PHOTO = "https://lh3.googleusercontent.com/as4imQyXpEaNg1dP7p7_lyImIAeVE_iOvzw7bLN_d_SREsNW_jsWMfVA3ORChgIfKpB1HmGWBv9xgw2JFdc3MxsxRWihFCPr_BhBXzkBIqOAfBRSFzMna-zYMXu2wQpPi-svrN2eTn4MhXz06Asc4ITtaf6HRj92gafP5kvD7PDFYP-FXb5uhlYFe25xAoEzq9j4iaoAj_XtONmetFZTko-aBn4IvvSNQOtBEYecvbhcU88zJQ0BWY9F315TVjxH3NnSIdPLtEHsuMqhpcOs643hoQKlNnK5faxu07PRGwyZq9tJNUI_Z_0zEmfups8_NuV2chwxtK5dN_Zk90zb51Y__CnXZxcwuX9dSGz5MIwgQM7-Oc8EWHTf_T5AzjzoyHKpskt0SkXGWeLt_nvTAvuASgL5r5AFrun1_Ogo16-wltRCPGphfshVO1d-s8ZULhVXqg_lV2pb0jwfKuT2701ItJTibP5ZDLLqwXOZVCyeedh3slFXAoN5MSEBka_SWhhncBdNHL1jhVE2UiuiMpBSGoABBIXWxG7u7MeheQj2=w431-h450-no"
    PERSONAL_PHOTO = "https://lh3.googleusercontent.com/sJHyj6IMbBK4Q2RJxakBiUE8keerizsZxuZQUnDIneUKhIO4tC_oUyfE259oW0LFREuPgWd5RMVc6-yjY9v_jA4aUDmGLpTbL8xOwY6rLO7v9yW3Dg6MeorFJgkHjvUK1awSn486BZlvECvK9mEiogRx1UYLayIUw5BodQmaDxGjWijuNmNUPYxt9b1ShE0clb0gycJsnJXh31guWlCyEac4rI5vSqfdahYHL5MBgDpXi9zP_u3rwfdM2MkFuEmqaqw60Dglb8kpZggbDROKgDRT3pEeYK4bo-IgXND47PzwxOkbAXwd1rMCw6_gDHOjw0Yvl82xsTSlJVGDEuLu7DRpNJGlebzyN5xZLtzW_WibLMVNx2GHfMeTjbHO1j7LJQyxTKR18NS1eVqhx5dkuktAPjnA5bLhx069xkEMKyH28NIOHlD0Vk66UHgtJKFNB7R7zHfW-VFnM64oCleYkDdw1ztOanSngRSHcwmdZl3k9zh4-ChfLeh31EJ8OzkCca_wxj6LOx-WvsOc8lydih2EcnXG-Bi_hAzNuVcNftuK=w431-h450-no"
    #PERSONAL_PHOTO = "https://lh3.googleusercontent.com/Jqffg3oDlUR61GHHRnc2W7Zmp5pTIZt0OPKnT1bG-FSBWSyBCayDsC-MJfgPhk4NKeYwd67t4EqMeDBCdzPISpL2qFf1LxEWyrYr2mvCJwj2tIrudB_sJBZRRwdKRkml8E6ntL80L0A6AzstUL6aJ50-X6h0RcMH0Q77vJm7FR6AhtSq67Rmcg91y-IP441aT70ovABjFaSISZqMlIeCLIPk_OUgJdb8zMh96Bfk5ePvISIC7sSwnwDVmu3bR301l9k8zdX98oa7WhfrBx-hzvgb3k9WDrtRL96NdPsy4mUFMJ7MxdMUflq9hmnXoHz3d1mZfC1FoE-_L_XpZbpvTaCPmu2Ov8-JUlZ18jo1w7kIFbkyNSC5GqebVquKXUYPWBlHq3m5zGHY5rRpodSQg5Zj3DBVLOLDasPiPY7NJbOHxAL8drEcM3kIdgPltPydl_NCAZ6OWO4szGVJcXd71ly6qJAKRF1P2MGGcLcZE8EpiSqE71VTIyfthctvmPLhBJFC9kr_pSwTskdcnkeH6uRAQDrb8dM0QOkKYV5p-8a9=w545-h568-no"
    
    workLinks = ['http://www.pawsey.org.au/',
                 'http://pyctqw.readthedocs.org',
                 'http://australiangeographic.com.au']

    WORK_DESCRIPTION = """
    <p style="text-align:left"> My current research interests mainly lie in the characterisation and applications of quantum walks, 
    with specific focus on quantum simulation of complex biochemical systems such as photosynthesis 
    and electron transport in functional nano-materials.<br><br>

    A major part of my research involves numerical simulation on high performance supercomputing 
    clusters (mainly using the <a href={0}>Pawsey</a> supercomputing facility in Western Australia), 
    working mostly with Fortran and Python. In order to streamline my workflow, I developed an efficient 
    parallel framework for simulating continuous-time quantum walks, <a href={1}>pyCTQW</a>, with the 
    source code available on my GitHub page. Other tools I find useful for my work include iPython, 
    matplotlib, the amazingly extendable SublimeText, and of course Mathematica and $\LaTeX{{}}$.<br><br>

    Outside of research, I am also employed as a tutor, lab demonstrator, and guest lecturer for 
    undergraduate and honours physics units at UWA.

    I also enjoy science writing and communication - my writing has so far been featured in 
    <a href={2}>Australian Geographic</a>.</p>
    """.format(*workLinks)

    WORK_PUBLICATIONS = True

    WORK_LIST = [['link',
                'http://d3lp4xedbqa8a5.cloudfront.net/s3/digital-cougar-assets/AusGeo/2015/10/12/59099/why-do-female-birds-sing.jpg',
                'Female fairy-wrens sing for other females',
                'Article published in Australian Geographic',
                'http://www.australiangeographic.com.au/news/2015/10/why-do-female-birds-sing-%281%29'],
                ['link',
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

