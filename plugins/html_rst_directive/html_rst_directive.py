# -*- coding: utf-8 -*-
"""
HTML tags for reStructuredText
==============================

This plugin allows you to use HTML tags from within reST documents. 

"""

from __future__ import unicode_literals
from docutils import nodes, utils
from docutils.parsers.rst import directives, Directive, roles


class RawHtml(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def run(self):
        html = ' '.join(self.content)
        node = nodes.raw('', html, format='html')
        return [node]

class Math(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def run(self):
        html = '\\begin{align}\n' \
        		+ ' '.join(self.content) \
        		+ '\n\\end{align}'
        node = nodes.raw('', html, format='html')
        return [node]

def math_role(role, rawtext, text, lineno, inliner,
                       options={}, content=[]):

    node = nodes.raw('', '$'+utils.unescape(rawtext[7:-1])+'$', format='html')
    return [node], []

def register():
    directives.register_directive('html', RawHtml)
    directives.register_directive('math', Math)
    roles.register_canonical_role('math', math_role)

