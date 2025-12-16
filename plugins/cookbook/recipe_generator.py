import os
import logging
from pelican.contents import Page
from pelican.generators import Generator
from pelican import signals
from jinja2 import Template
import re
from bs4 import BeautifulSoup  # New import

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
        soup = BeautifulSoup(recipe._content, "html.parser")

        # Initialize sections
        recipe.intro_html = ""
        recipe.ingredients_html = ""
        recipe.method_html = ""
        recipe.notes_html = ""

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
            # Check if we hit a new header
            if tag.name == "h2":
                header_text = tag.get_text().strip().lower()
                if header_text in section_map:
                    current_section = section_map[header_text]
                    continue  # Don't include the <h2> tag itself in the content

            # Append the tag to the current section string
            # We convert the tag back to string to preserve HTML
            setattr(recipe, current_section, getattr(recipe, current_section) + str(tag))

        if recipe.ingredients_html:
            # Regex explanation:
            # \(        -> Look for literal opening parenthesis
            # [^)]+     -> Match 1 or more characters that are NOT a closing parenthesis
            # \)        -> Look for literal closing parenthesis
            # The outer () capture the whole group so we can reference it with \1
            recipe.ingredients_html = re.sub(
                r"(\([^)]+\))", r'<span class="paren">\1</span>', recipe.ingredients_html
            )

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
