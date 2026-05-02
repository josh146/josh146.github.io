import os
import logging
from pelican.generators import Generator, ArticlesGenerator, PagesGenerator
from pelican import signals
import json
import yaml

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


def generate_search_index(generators):
    """
    Generates a JSON file containing all recipes and pages for the search palette.
    """
    article_generator = next((g for g in generators if isinstance(g, ArticlesGenerator)), None)
    page_generator = next((g for g in generators if isinstance(g, PagesGenerator)), None)
    recipe_generator = next((g for g in generators if isinstance(g, RecipeGenerator)), None)

    if not article_generator:
        return

    search_data = []

    # add Pages
    if page_generator:
        for page in page_generator.pages:
            if page.title != "hello.":
                search_data.append(
                    {"title": fix_string(page.title), "url": f"/{page.url}", "type": "Pages"}
                )

    search_data += [{"title": "Posts.", "url": "/posts", "type": "Pages"}]

    # add Recipe
    for recipe in recipe_generator.recipes:
        search_data.append(
            {
                "title": fix_string(recipe.title),
                "url": f"/{recipe.url}",
                "type": "Recipes",
                "keywords": f"{recipe.category}" + " ".join([t.name for t in getattr(recipe, "tags", [])]),
            }
        )

    # add articles
    for article in article_generator.articles:
        # We assume anything in the 'Recipes' category or with type='recipe' is a recipe

        search_data.append(
            {
                "title": fix_string(article.title),
                "url": f"/{article.url}",
                "type": "Articles",
                "keywords": " ".join([t.name for t in getattr(article, "tags", [])]),
            }
        )

    # Find the cookbooks.yaml file in your content folder
    content_path = article_generator.settings.get('PATH', 'content')
    yaml_path = os.path.join(content_path, 'cookbooks.yaml')

    if os.path.exists(yaml_path):
            with open(yaml_path, 'r', encoding='utf-8') as f:
                try:
                    cookbooks = yaml.safe_load(f) or []
                    for book in cookbooks:
                        book_title = book.get('book', 'Unknown Book')

                        for recipe in book.get('recipes', []):
                            search_data.append({
                                'title': recipe.get('title', ''),
                                'url': '#', # No URL, it's a physical book
                                'type': 'Physical',
                                'book': book_title,
                                'page': recipe.get('page', ''),
                                'ingredient': recipe.get('ingredient', ''),
                            })
                except Exception as e:
                    print(f"Error parsing cookbooks.yaml: {e}")

    # write to output/search.json
    output_path = os.path.join(article_generator.output_path, "search.json")
    os.makedirs(article_generator.output_path, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(search_data, f)

def expose_cookbooks_to_jinja(generator):
    """
    Reads cookbooks.yaml and makes it available as the {{ COOKBOOKS }}
    variable in all Jinja templates.
    """
    content_path = generator.settings.get('PATH', 'content')
    yaml_path = os.path.join(content_path, 'cookbooks.yaml')

    cookbooks_data = []
    if os.path.exists(yaml_path):
        with open(yaml_path, 'r', encoding='utf-8') as f:
            try:
                cookbooks_data = yaml.safe_load(f) or []
            except Exception as e:
                print(f"Error reading cookbooks.yaml for Jinja: {e}")

    # Attach to the global Jinja context
    generator.context['COOKBOOKS'] = cookbooks_data


def get_generators(pelican_object):
    return RecipeGenerator


def register():
    signals.page_generator_init.connect(expose_cookbooks_to_jinja)
    signals.get_generators.connect(get_generators)
    signals.all_generators_finalized.connect(generate_search_index)
