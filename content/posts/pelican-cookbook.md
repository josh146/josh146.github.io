Title: Building a vintage recipe rolodex with Python, Pelican, and Markdown.
Slug: pelican-cookbook-markdown-recipes
Date: 2026-05-18 16:00
Tags: python
Category: cooking
Author: Josh Izaac

I enjoy cooking. Not only that, but I enjoy **complicated** cooking --- which can sometimes be a bit of a curse.

A simple weeknight meal? Not interested. A week-long project to nail the ultimate [Xiao Long Bao](/recipes/chicken-xiao-long-bao/), [Croissants](/recipes/pate-a-croissant/), or [homemade ramen](/recipes/duck-paitan-ramen/)?
Sign me up! I become somewhat obsessive, reading cooking blogs,
cookbooks, and YouTube videos to figure out not just the baseline techniques and ingredients, but
the endless *variations* between them. And as I refine a recipe and my method, I make sure to write
down what worked (and what didn't!).

In the beginning, my method was to use Microsoft Publisher and generate a PDF (to be fair, it was
2004). As my physics career took off and I became surrounded by open-source tech and tooling, this
transitioned to PDFs generated from simple Markdown files stored in Dropbox.

But this setup had its flaws. PDFs don't render well on mobile phones, and Dropbox isn't exactly the
ideal platform for seamlessly maintaining, updating, and sharing a repository of recipes. At the
time, I had already created this website, which was built on [Pelican](https://getpelican.com/) --- a static-site generator for Python built on Markdown files. Since I
already had an affinity for Markdown, I figured there must surely be a library that allows me to
store and version my recipes using Markdown and Git, yet still render them for easy browsing and
searching.

<img src="/images/recipes/recipe-card.jpg" style="max-width: 800px; width: 100%;" />

From what I could find... not really.

The two most promising options were [Chowdown](https://github.com/clarklab/chowdown) (however, I wanted to avoid a Jekyll-based solution) and [Jeff Thompson's Recipe Website](https://github.com/jeffThompson/recipes/) (I loved the style, but wanted a static site generator). There were also a couple of cloud services and phone apps that store recipes in Markdown formats (such as [Tandoor](https://tandoor.dev/) and [Grocery](https://apps.apple.com/us/app/grocery-smart-shopping-list/id1195676848)), but I didn't want to be tied down to one platform or depend on paid tiers just to get the most out of my Markdown files.

So, armed with a researcher's knowledge of Jinja, Python, JavaScript, and CSS, I thought: *why not build it myself?*

## The Pelican Cookbook plugin

I started this project with a few core goals:

1. **Plain text format**: Recipes need to be stored as plain text and remain **readable**.

2. **Can be rendered as HTML**: They should render nicely as static HTML with a minimalist theme,
allowing readers to get right to the point: the ingredients list and the steps.

3. **Cross-references and components:** Recipes need to be able to cross-reference each other, and
even embed each other as components (to avoid writing out the same sub-recipes over and over!).

4. **Timelines**: It needs to be easy to extract information about complex recipes. If I can only
start cooking at 4:45 PM, what time will I be eating?

5. **Search:** Both recipes and individual ingredients need to be **searchable**.

Using the following Markdown format for a recipe keeps everything highly readable, with perhaps the
exception of some website-specific YAML frontmatter at the top:

```markdown
Title: Lime curd
Date: 2025-12-24
Category: Sweets
Slug: lime-curd
Time: 30 minutes
Servings: 750ml
Image: /images/recipes/lime-curd.jpg

## Ingredients

* 115g unsalted butter (cut into 1cm cubes)
* 180ml freshly-squeezed lime juice (about 5-6 limes)
* 140g sugar
* zest of two limes, unsprayed (see Note)
* pinch of salt
* 3 large egg yolks
* 3 large eggs

## Steps

1. In a glass bowl over a saucepan filled with simmering water, warm the butter, lime juice, sugar,
zest, and salt.

1. In a separate bowl, whisk together the eggs and the yolks.

1. When the butter has melted and the mixture is warm, gradually pour some of the warm lime juice
mixture into the eggs, whisking constantly. Scrape the warmed eggs back into the double boiler and
cook the mixture over low heat.

1. Stir the mixture constantly over low heat, using the whisk, until the filling thickens and begins
to resemble soft jelly. Do not let it boil. When done, strain the curd through a fine-mesh sieve.
```

You can see the [raw Markdown file on GitHub](https://github.com/josh146/josh146.github.io/blob/source/content/recipes/lime-curd.md), and the
[resulting rendered page](/recipes/lime-curd/). This easily hits points (1) and (2).

To solve point (3), I added the ability to use `[[Recipe title]]` to insert an automatic
cross-reference to other recipes. Going one step further, you can use `[[Component: recipe title]]`
within an ingredients list or method in order to insert another recipe's instructions *directly*
into the current one!

```markdown
Title: Lime meringue tart
Date: 2025-12-19
Category: Pastry
Slug: lime-meringue-tart
Time: 1 hour
Servings: 1 9-inch (22cm) tart
Image: /images/recipes/lime-meringue-tart.jpg
Tags: dessert

## Ingredients

* 1 blind-baked [[Pâte Sablée]] tart shell.
[[Component: lime curd]]
[[Component: swiss meringue]]

## Instructions

1. Preheat the oven to 180ºC.

[[Component: lime curd]]

1. Pour the curd into the pre-baked tart shell, and bake for 10 minutes.

[[Component: swiss meringue]]
```

What about cooking timelines?

Simply include the `Timeline` metadata:

```markdown
Timeline: Mix Ingredients | 15m | Active; First proof | 60m | Wait; Second proof | 45m | Wait; Shape | 15m | Active; Proof | 60m | Wait; Bake | 30m | Wait
```

and a cooking schedule calculator will magically appear at the top of the [rendered recipe page](/recipes/challah).

<img src="/images/cooking-schedule.png" style="max-width: 600px; width: 100%;" />

You can even dynamically change the start time as needed, and the schedule will automatically
update.

Finally, [search was enabled](/search) through the use of the [Ninja Keys](https://github.com/ssleptsov/ninja-keys) package. This enables searching of not just recipe titles, but ingredients as well (including support for more complex Google-style search syntax to find recipes with specific combinations of ingredients).

## Intuitive cooking

A conclusion I have slowly come to over time is that cooking is less of a science, and much more of
an art. Even in disciplines like baking, where we often hear the refrain "baking is a science!"
(and see a growing number of technically-minded people moving into the space aiming to explore and
quantify every variable), I remain unconvinced.

If that were true, we would have all arrived at the singular, perfect choux pastry or wholemeal
sourdough recipe by now. Instead, we have incredible variation where the ingredient ratios are
similar, yet can still differ quite significantly.

Instead, cooking is **intuitive** --- with frameworks such as rough ratios and known flavor
combinations, it is easy to riff on recipes and ideas to come up with something entirely new
(and delicious!).

But how do you account for this with a repository of Markdown files, which are somewhat rigid by
definition?

One final feature I added is the concept of **blueprint recipes**. While a bit messier under the
hood, this allows you to provide various flavor variations within the Markdown via embedded YAML:

```markdown
<pre id="variation-yaml" style="display:none;">
Theme: Cardamom and onion
marinade: olive oil, cardamom, cloves, cinnamon sticks, salt, and pepper
marinade_list: 30ml olive oil (2 tbsp); 10 cardamom pods; 1/3 tsp whole cloves; 2 long cinnamon sticks, broken in two; 1.5 tsp salt; 1.5 tsp pepper
aromatics: sliced onions
aromatic_list: 2 onions (sliced); 30ml olive oil (2 tbsp)

---

Theme: Biriyani
marinade: mustard oil, minced ginger and garlic, kashmiri chilli powder, salt, and spices,
marinade_list: 1 tsp mustard oil; 1 inch ginger (grated); 4 garlic cloves (grated); 1 tbsp kashmiri chilli powder; 1 tbsp garam masala; 1 tbsp cumin; 1 tbsp coriander; juice of 1 lemon; 1.5 tsp salt
aromatic_list: 50g butter or oil; 1 red onion (finely diced); 1 inch ginger (grated); 4 cloves garlic (grated); 1 tomato (finely diced); 1 tsp garam masala; 1 tsp tumeric
aromatics: onion, ginger and garlic mixture, tomato, and spices
</pre>
```

Within the standard Markdown recipe, you can then use these defined variables (`{{aromatics}}`, `{{marinade_list}}`, etc.). Users can pick their "vibe" and watch the recipe update dynamically—all
driven from a single Markdown file.

You can check this out on my [one-pot chicken rice recipe](/recipes/one-pot-chicken-and-rice/), and see the [associated Markdown file](https://github.com/josh146/josh146.github.io/blob/source/content/recipes/one-pot-chicken-rice.md).

## Why did you mention vintage recipe cards?

At the very top of this post, I included a picture of a recipe index card from the 1950s for corned
beef and cabbage. This card belonged to my maternal grandmother. I spent a while attempting to
decipher her handwriting and reverse-engineer the recipe based on the versions I remember from my
childhood ([which you can find here](/recipes/corned-beef)).


To me, this bootstrapped Markdown-Python-Jinja-Javascript recipe rolodex is no different from those
index cards. I wanted my digital collection to hearken back to those days. The modern internet and
food media landscape is a double-edged sword; we are incredibly lucky to be able to access recipes
from cuisines all over the world in seconds, yet we are far less likely to write down our own
recipes and pass them on to our loved ones, the way [our grandparents did for us](https://www.reddit.com/r/oldrecipes/) (and [their grandparents for them](https://www.handwrittenwork.com/handwritten-recipes)!).


For me, this sentiment is close to my heart for one very specific reason. Growing up in the very
small Singaporean-Iraqi Jewish community, the food of my childhood is a highly specific fusion of
flavors, ingredients, and cultures. It simply does not exist online; it is solely passed down
through lived experience. Recipes such as [Bamya Assam](/recipes/bamya-assam) and [Beetroot stew](/recipes/beetroot-stew/) meld Singaporean ingredients with Iraqi Jewish cooking methods, and if we do
not write them down, they might be lost entirely.

I hope my little janky, Markdown-backed static recipe website will keep this tradition going just a
little bit longer.