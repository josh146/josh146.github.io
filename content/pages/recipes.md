Title: Recipes.
slug: recipes
save_as: recipes.html

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

