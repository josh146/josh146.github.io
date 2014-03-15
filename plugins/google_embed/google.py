# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from docutils import nodes
from docutils.parsers.rst import directives, Directive
from pelican import signals

def content_object_init(instance):

    GMAPS_KEY = instance.settings['GMAPS_KEY']

    class GPlusCard(Directive):
        required_arguments = 1
        optional_arguments = 0

        final_argument_whitespace = True
        has_content = True

        def run(self):
            url = self.arguments[0].strip()

            scriptHTML = "<script type='text/javascript' src='https://apis.google.com/js/plusone.js'></script>"
            linkHTML = "<div class='g-post' data-href='{}'></div>".format(url)

            return [nodes.raw('', scriptHTML, format='html'),
                    nodes.raw('', linkHTML, format='html')]


    class GMapsCard(Directive):


        def mode(argument):
            """Conversion function for the "align" option."""
            return directives.choice(argument, ('place', 'search', 'directions'))

        def maptype(argument):
            """Conversion function for the "align" option."""
            return directives.choice(argument, ('roadmap', 'satellite'))

        required_arguments = 0
        optional_arguments = 1
        option_spec = {
            'mode': mode,
            'width': directives.positive_int,
            'height': directives.positive_int,
            'maptype': maptype,
        }

        final_argument_whitespace = True
        has_content = True

        def run(self):
            location = '+'.join(self.arguments[0].split())
            mode = "place"
            maptype = "roadmap"
            width = 600
            height = 400

            if 'mode' in self.options:
                mode = self.options['mode']
            if 'maptype' in self.options:
                maptype = self.options['maptype']
            if 'width' in self.options:
                width = self.options['width']
            if 'height' in self.options:
                height = self.options['height']

            linkHTML="""
                <iframe
                  width="{3}"
                  height="{4}"
                  frameborder="0" style="border:0"
                  src="https://www.google.com/maps/embed/v1/{0}?key={1}
                    &q={2}&maptype={5}">
                </iframe>
                """.format(mode,GMAPS_KEY,location,width,height,maptype)

            return [nodes.raw('', linkHTML, format='html')]


    class GMapsDirections(Directive):

        def mode(argument):
            """Conversion function for the "align" option."""
            return directives.choice(argument, ('driving',
                'walking',
                'bicycling',
                'transit',
                'flying'))

        def maptype(argument):
            """Conversion function for the "align" option."""
            return directives.choice(argument, ('roadmap', 'satellite'))

        required_arguments = 0
        optional_arguments = 1
        option_spec = {
            'mode': mode,
            'width': directives.positive_int,
            'height': directives.positive_int,
            'maptype': maptype,
            'origin': directives.unchanged,
            'destination': directives.unchanged,
            'waypoints': directives.unchanged,
        }

        final_argument_whitespace = True
        has_content = True

        def run(self):
            mode = ""
            waypoints = ""
            maptype = "roadmap"
            width = 600
            height = 400

            if 'mode' in self.options:
                mode = self.options['mode']

            if 'maptype' in self.options:
                maptype = self.options['maptype']

            if 'width' in self.options:
                width = self.options['width']

            if 'height' in self.options:
                height = self.options['height']

            if 'origin' in self.options:
                origin = '+'.join(self.options['origin'].split())

            if 'destination' in self.options:
                destination = '+'.join(self.options['destination'].split())

            if 'waypoints' in self.options:
                waypoints = '+'.join(self.options['waypoints'].split())
                linkHTML="""
                    <iframe
                      width="{1}"
                      height="{2}"
                      frameborder="0" style="border:0"
                      src="https://www.google.com/maps/embed/v1/directions?key={0}
                        &origin={4}&destination={5}&waypoints={6}&maptype={3}&mode={7}">
                    </iframe>
                    """.format(GMAPS_KEY,width,height,maptype,origin,destination,waypoints,mode)
            else:
                linkHTML="""
                    <iframe
                      width="{1}"
                      height="{2}"
                      frameborder="0" style="border:0"
                      src="https://www.google.com/maps/embed/v1/directions?key={0}
                        &origin={4}&destination={5}&maptype={3}&mode={6}">
                    </iframe>
                    """.format(GMAPS_KEY,width,height,maptype,origin,destination,mode)


            return [nodes.raw('', linkHTML, format='html')]

    directives.register_directive('gplus', GPlusCard)
    directives.register_directive('gmaps', GMapsCard)
    directives.register_directive('directions', GMapsDirections)

def register():
    signals.content_object_init.connect(content_object_init)

