# Pelican cookbook plugin

This plugin allows you to use Pelican as a static cookbook generator.

## Getting started

Add the following to your `pellicanconf.py` file:

```python
ARTICLE_EXCLUDES = ['recipes']
RECIPE_URL = 'recipes/{slug}/'
RECIPE_SAVE_AS = 'recipes/{slug}/index.html'
```

and make sure `"cookbook"` is listed in the `PLUGINS` list.

Then:

- Create a page `recipes.md` on your site, and add a recipe gallery.
- Create a folder `content/recipes` to store your recipes.

## Recipe format

Recipes are of the format

```markdown
Title: Lime Meringue Tart
Date: 2025-12-19
Category: Pastry and dessert
Slug: lime-meringue-tart
Time: 1 hour
Servings: 1 9-inch (22cm) tart
Image: /images/recipes/lime-meringue-tart.jpg
Sticky: true

Intro to recipe.

## Ingredients

* 115g unsalted butter (cut into 1cm cubes)
* 180ml freshly-squeezed lime juice (about 5-6 limes)
* 140g sugar
* zest of two limes, unsprayed (see Note)
* pinch of salt
* 3 large egg yolks
* 3 large eggs

## Steps

1. Preheat the oven to 180ºC.

2. In a glass bowl over a saucepan filled with simmering water, warm the butter, lime juice, sugar,
zest, and salt.

3. In a separate bowl, whisk together the eggs and the yolks.

## Notes

The tart is best eaten the day it is made. You can refrigerate any leftovers. If you wish to make
the lime filling in advance, you can make it and store it in the refrigerator for up to five days.
```

You can use h3 headers (`###`) to separate sections in the ingredients list and method list.

## Features

- Footnotes: use `[ref]Insert footnote here.[/ref]` to place footnotes. You will need a `## Notes`
  header so they can be rendered properly.

- Sticky: set this to true to allow the ingredients list to stay sticky on the page.

- Cross reference links: use ``[[Recipe title]]`` to insert an automatic cross reference to other
  recipes.

- Components: use ``[[Component: recipe title]]`` within the ingredients list or method list in
  order to insert another recipes ingredients/method into the current one.

- Cooking timline: Add the metadata `Timeline:` of the form

  ```markdown
  Timeline: Mix Ingredients | 15m | Active; First proof | 60m | Wait; Second proof | 45m | Wait; Shape | 15m | Active; Proof | 60m | Wait; Bake | 30m | Wait
  ```

  to insert a cooking schedule timeline onto the page. The format is `description of the step | time
  | Active or Wait`. `time` can use `m`, `h`, or `d` to indicate minutes, hours, or days. Steps
  should be separated with semi-colons.

## Blueprint recipes

Blueprint recipes allow you to provide a 'template' recipe with items to be filled in by the reader.
You can also provide pre-populated template variations as well.

- Insert the variation controls somewhere on the page: `<div id="variation-controls"></div>`

- Use blueprint variables within the ingredients and the method, e.g., `{{aromatics}}`. These will
  be replaced when a variation is selected.

- Define your variations:

  <pre id="variation-yaml" style="display:none;">
  Theme: Tomato and garlic
  vegetables: tomatoes, shallots, garlic cloves, coriander stems, dill,
  vegatable_list: 750g cherry tomatoes; 4 large shallots (roughly chopped); 12-15 garlic cloves; 4 small cinnamon sticks; 20g coriander stems (cut into 4 cm lengths); 20g dill (roughly chopped)
  ---

  Theme: Bamya assam
  vegetables: tomatoes, okra, shallots, garlic cloves, ginger, coriander stems, lemon juice, tumeric,
  vegatable_list: 4 large shallots (roughly chopped); 8 garlic cloves; 1 inch ginger (grated); 10 okra; 4 small cinnamon sticks; 20g coriander stems (cut into 4 cm lengths); 20g mint (roughly chopped); juice from 2 lemons; 1 tsp tumeric
  ---

  Theme: Mushroom and thyme
  vegetables: mushrooms, shallots, garlic cloves, coriander stems, dill,
  vegatable_list: 500g assorted mushrooms; 4 large shallots (roughly chopped); 12-15 garlic cloves; 20g thyme (roughly chopped)
  </pre>

  Variables ending with `_list` are semi-colon separated lists, and will be rendered as a bullet
  point list. This is useful for adding ingredients to the variations. Note that list variables are
  not rendered as part of the default blueprint view.

