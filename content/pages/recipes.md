Title: Recipes.
slug: recipes
save_as: recipes.html
og_title: Josh Iza.ac
og_description: I'm a computational quantum physicist and software developer, working to build accessible, open-source quantum software at Xanadu, a Toronto-based quantum photonic hardware company.
og_image: https://iza.ac/images/header-small.png

Here you can find a collection of my recipes, ranging from savoury to dessert to bread.

{% for group in recipes|groupby("category") %}
<h2 class="recipe-category">{{ group.grouper }}</h2>
<ul>
{% for recipe in group.list %}
    <li>
        <a href="{{ recipe.url }}">{{ recipe.title }} </a>
    </li>
{% endfor %}
</ul>

{% endfor %}

