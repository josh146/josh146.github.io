from __future__ import unicode_literals
from markdown.inlinepatterns import Pattern
from markdown.extensions import Extension

EMBED_REGEX = '\[!pic(\?(.*))?\]\((.*)\)'


class BetterPicEmbedPattern(Pattern):

    def __init__(self, md):
        super(BetterPicEmbedPattern, self).__init__(EMBED_REGEX)
        self.md = md

    def handleMatch(self, m):
        url = m.group(4)

        if m.group(3) is not None:
            parameters = dict([i.split('=') for i in m.group(3).split('?')])
        else:
            parameters = {}

        if 'caption' in parameters:
            caption = parameters['caption']
        else:
            caption = None

        if 'alt' in parameters:
            alt = parameters['alt']
        else:
            alt = "picture"

        if 'height' in parameters:
            height = "height: {}px".format(parameters['height'])
        else:
            height = "height: auto"

        if 'width' in parameters:
            width = "width: {}px".format(parameters['width'])
        else:
            width = "max-width: 100%"

        if caption is not None:
            picHTML = """
                <center>
                    <img style="{2}; {3};" src='{0}' alt='{1}'></img>
                    <h4><div align=center><em>{4}</em></div></h4>
                </center>
            """
        else:
            picHTML = """
                <center>
                    <img style="{2}; {3};" src='{0}' alt='{1}'></img>
                </center>
            """

        return self.md.htmlStash.store(picHTML.format(url,alt,height,width,caption))


class BetterPicEmbedExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('pic', BetterPicEmbedPattern(md), '_begin')


def makeExtension(configs=None):
    return BetterPicEmbedExtension(configs)
