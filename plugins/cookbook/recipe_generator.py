import os
import logging
from pelican.contents import Page
from pelican.generators import Generator
from pelican import signals
from jinja2 import Template
import re
from bs4 import BeautifulSoup

from .parse_footnotes import parse_footnotes


log = logging.getLogger(__name__)


class Recipe(Page):
    """
    A custom content object for Recipes.
    """

    default_template = "recipe"


class RecipeGenerator(Generator):
    """
    Walks through content/recipes and generates Recipe objects.
    """

    def __init__(self, *args, **kwargs):
        super(RecipeGenerator, self).__init__(*args, **kwargs)
        self.recipes = []

    def generate_context(self):
        # Define path to recipes folder
        recipe_path = os.path.join(self.settings["PATH"], "recipes")

        for root, dirs, files in os.walk(recipe_path):
            for filename in files:
                if filename.endswith(".md"):
                    source_path = os.path.join(root, filename)

                    try:
                        recipe_item = self.readers.read_file(
                            base_path=self.path,
                            path=source_path,
                            content_class=Recipe,
                            context=self.context,
                        )

                        parse_footnotes(recipe_item)

                        self._parse_recipe_sections(recipe_item)
                        self.recipes.append(recipe_item)
                    except Exception as e:
                        log.error(f"Could not read recipe {filename}: {e}")

        # Sort recipes alphabetically by title
        # self.recipes.sort(key=lambda x: x.title)

        # Sort recipes by category
        self.recipes.sort(key=lambda x: (str(x.category), x.title))

        # Inject into global context
        self.context["recipes"] = self.recipes
        self.context["Recipe"] = Recipe

    def _parse_recipe_sections(self, recipe):
        """
        Splits the content into intro, ingredients, method, and notes.
        Stores them as attributes on the recipe object.
        """
        if hasattr(recipe, 'timeline'):
            self._parse_timeline(recipe)

        soup = BeautifulSoup(recipe._content, "html.parser")

        # Initialize sections
        recipe.intro_html = ""
        recipe.ingredients_html = ""
        recipe.method_html = ""
        recipe.notes_html = ""
        recipe.footnotes_html = ""  # Store footnotes here

        # Initialize raw lists for Schema
        recipe.ingredients_list = []
        recipe.instructions_list = []

        # Standardize headers to look for (lowercase for comparison)
        section_map = {
            "ingredients": "ingredients_html",
            "method": "method_html",
            "steps": "method_html",
            "instructions": "method_html",  # Handle synonyms
            "notes": "notes_html",
        }

        current_section = "intro_html"

        # Iterate over all top-level elements
        for tag in soup:
            # Get safe tag name
            tag_name = getattr(tag, 'name', None)

            # check for Section Headers
            if tag_name == 'h2':
                header_text = tag.get_text().strip().lower().rstrip(':')
                if header_text in section_map:
                    current_section = section_map[header_text]
                    continue

            # Append the tag to the current section string
            # We convert the tag back to string to preserve HTML
            setattr(recipe, current_section, getattr(recipe, current_section) + str(tag))

        if recipe.ingredients_html:
            ing_soup = BeautifulSoup(recipe.ingredients_html, 'html.parser')
            # Find all list items (li) and get their text
            recipe.ingredients_list = [li.get_text().strip() for li in ing_soup.find_all('li')]

        if recipe.method_html:
            method_soup = BeautifulSoup(recipe.method_html, 'html.parser')

            # FIX: Prioritize List Items (<li>)
            # Only look for <p> if no <li> tags are found.
            # This prevents double counting when <li> contains <p>.

            steps = method_soup.find_all('li')

            if not steps:
                # Fallback: If the user didn't use a list, look for paragraphs
                steps = method_soup.find_all('p')

            recipe.instructions_list = [s.get_text().strip() for s in steps]

            # Clean up empty strings just in case
            recipe.instructions_list = [i for i in recipe.instructions_list if i]

        if recipe.ingredients_html:
            recipe.ingredients_html = self._apply_scaling_to_html(recipe.ingredients_html)

            # Regex explanation:
            # \(        -> Look for literal opening parenthesis
            # [^)]+     -> Match 1 or more characters that are NOT a closing parenthesis
            # \)        -> Look for literal closing parenthesis
            # The outer () capture the whole group so we can reference it with \1
            recipe.ingredients_html = re.sub(
                r"(\([^)]+\))", r'<span class="paren">\1</span>', recipe.ingredients_html
            )

    @staticmethod
    def _parse_duration_string(duration_str):
        """
        Converts '1h 30m', '2 hours', '45' into total integer minutes.
        """
        duration_str = duration_str.lower().strip()

        # If it's just a number, assume minutes (legacy support)
        if duration_str.isdigit():
            return int(duration_str)

        total_mins = 0
        label = ""

        # Check for Days
        days = re.search(r'(\d+)\s*d', duration_str)
        if days:
            d = int(days.group(1))
            total_mins += d * 24 * 60

            if d == 1:
                label += f"{d} day "
            else:
                label += f"{d} days "

        # Check for Hours
        hours = re.search(r'(\d+)\s*h', duration_str)
        if hours:
            h = int(hours.group(1))
            total_mins += h * 60

            if h == 1:
                label += f"{h} hour "
            else:
                label += f"{h} hours "

        # Check for Minutes
        mins = re.search(r'(\d+)\s*m', duration_str)
        if mins:
            m = int(mins.group(1))
            total_mins += m
            label += f"{m} min"

        return total_mins, label

    @staticmethod
    def _parse_timeline(recipe):
        # We convert it into a list of dictionaries.
        parsed_timeline = []
        current_offset = 0

        # 1. Force it to be a string and split by semicolon
        # Pelican reads "Step 1; Step 2" as a single string
        raw_string = str(recipe.timeline)

        # Split into individual steps
        steps = raw_string.split(';')

        for item in steps:
            # Skip empty items (e.g. if there is a trailing semicolon)
            if not item.strip():
                continue

            try:
                # Expected format: "Task | Duration | Type"
                parts = [p.strip() for p in item.split('|')]

                task_name = parts[0]

                duration_str = parts[1]
                duration_mins, label = RecipeGenerator._parse_duration_string(duration_str)

                # Default to 'active' if type is missing
                step_type = parts[2].lower() if len(parts) > 2 else 'active'

                parsed_timeline.append({
                    'task': task_name,
                    'duration': duration_mins,
                    'duration_display': label, # Keep original text for display
                    'type': step_type,
                    'start_offset': current_offset,
                    'end_offset': current_offset + duration_mins
                })

                current_offset += duration_mins

            except Exception as e:
                print(f"Error parsing timeline item '{item}': {e}")

        recipe.timeline_parsed = parsed_timeline
        recipe.total_duration_mins = current_offset

    def _apply_scaling_to_html(self, html_content):
        """
        Parses HTML, finds numbers in text nodes, and wraps them in spans.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        number_pattern = re.compile(r'(?<!\w)(\d+(?:[./]\d+)?)')

        for text_node in soup.find_all(string=True):
            # Skip numbers inside links, existing spans, or scripts
            if text_node.parent.name in ['a', 'script', 'style', 'sup']:
                continue

            # If we find a number, replace it
            if number_pattern.search(text_node):
                new_html = number_pattern.sub(
                    lambda m: self._make_scalable_span(m.group(0)),
                    text_node
                )
                # Replace the text node with the new HTML structure
                text_node.replace_with(BeautifulSoup(new_html, 'html.parser'))

        return str(soup)

    def _make_scalable_span(self, val_str):
        """Helper to create the HTML for the scalable number"""
        try:
            if '/' in val_str:
                num, den = val_str.split('/')
                base_val = float(num) / float(den)
            else:
                base_val = float(val_str)
            return f'<span class="scalable" data-base="{base_val}">{val_str}</span>'
        except ValueError:
            return val_str

    def generate_output(self, writer):
        for recipe in self.recipes:
            writer.write_file(
                recipe.save_as,
                self.get_template(recipe.template),
                self.context,
                page=recipe,
                relative_urls=self.settings.get("RELATIVE_URLS"),
                override_output=hasattr(recipe, "override_output"),
            )


def process_recipes_table(generators):
    """
    Runs after ALL generators are done.
    """
    if not generators:
        return

    # Get context from the first generator
    context = generators[0].context

    # 1. Safety check
    if "recipes" not in context or not context["recipes"]:
        return

    # 2. Find the 'recipes' page
    pages = context.get("pages", [])
    recipe_page = None

    for page in pages:
        if page.slug == "recipes":
            recipe_page = page
            break

    if not recipe_page:
        return

    # 3. Render the Jinja inside the recipes.md content
    try:
        # The Markdown reader converts content to HTML before we get here.
        # This often turns spaces inside {{ }} into &nbsp; which breaks Jinja.
        # We must clean the string before creating the Template.

        raw_content = recipe_page._content

        # Replace &nbsp; with a standard space
        # Optional: Fix other common encoding issues if they appear
        # raw_content = raw_content.replace('%20', ' ')
        raw_content = raw_content.replace("&nbsp;", " ")
        raw_content = raw_content.replace("&#8220;", "'")
        raw_content = raw_content.replace("&#8221;", "'")
        raw_content = raw_content.replace("&#8216;", "'")
        raw_content = raw_content.replace("&#8217;", "'")
        template = Template(raw_content)

        rendered_content = template.render(context)
        recipe_page._content = rendered_content

    except Exception as e:
        log.error(f"Error rendering recipes page: {e}")


def get_generators(pelican_object):
    return RecipeGenerator


def register():
    signals.get_generators.connect(get_generators)
    signals.all_generators_finalized.connect(process_recipes_table)
