import os
import logging
from pelican.generators import Generator
from pelican import signals
from jinja2 import Template
import re
from bs4 import BeautifulSoup

from .recipe import Recipe, RecipePostProcessor, fix_string


log = logging.getLogger(__name__)


class RecipeGenerator(Generator):
    """
    Walks through content/recipes and generates Recipe objects.
    """

    def __init__(self, *args, **kwargs):
        super(RecipeGenerator, self).__init__(*args, **kwargs)
        self.recipes = []
        self.recipes_index = {}

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

                        self.recipes.append(recipe_item)
                        self.recipes_index[fix_string(recipe_item.title.lower())] = recipe_item
                    except Exception as e:
                        log.error(f"Could not read recipe {filename}: {e}")

        # Sort recipes alphabetically by title
        # self.recipes.sort(key=lambda x: x.title)

        # Sort recipes by category
        self.recipes.sort(key=lambda x: (str(x.category), x.title))
        RecipePostProcessor(self.recipes, self.recipes_index)

        # Inject into global context
        self.context["recipes"] = self.recipes
        self.context["Recipe"] = Recipe
        self.context["recipes_index"] = self.recipes_index

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


def get_generators(pelican_object):
    return RecipeGenerator


def register():
    signals.get_generators.connect(get_generators)
