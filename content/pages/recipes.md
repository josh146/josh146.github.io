Title: Recipes.
slug: recipes
save_as: recipes.html
Description: Here you can find a collection of my recipes, ranging from savoury to dessert to bread.

<div class="recipe-intro">
    <div class="view-controls">
        <p style="margin: 0;">Here you can find a collection of my recipes, ranging from savoury to dessert to bread.</p>
    </div>
    <div class="view-controls">
        <button id="btn-gallery" class="view-btn active"><i class="fas fa-th"></i></button>
        <button id="btn-list" class="view-btn"><i class="fas fa-bars"></i></button>
    </div>
</div>

<div id="recipe-list" class="recipe-list hidden">
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
</div>

<div id="recipe-gallery" class="recipe-gallery">
{% for recipe in recipes %}
    <div class="recipe-card">
        <a href="{{ recipe.url }}">
            <div class="card-image-wrapper">
                {% if recipe.image %}
                <img src="{{ recipe.image }}" alt="{{ recipe.title }}">
                {% else %}
                <div class="no-image">🍳</div>
                {% endif %}
            </div>
            
            <div class="card-details">
                <h3>{{ recipe.title }}</h3>
                <div class="card-meta">
                    <span>{{ recipe.category }}</span>
                </div>
            </div>
        </a>
    </div>
{% endfor %}
</div>

<script>
// Get references to the button and the two elements
const btnGallery = document.getElementById('btn-gallery');
const btnList = document.getElementById('btn-list');
const gallery = document.getElementById('recipe-gallery');
const list = document.getElementById('recipe-list');

// Add a click event listener to the button
btnGallery.addEventListener('click', function() {
    // Toggle the 'hidden' class on both elements
    gallery.classList.toggle('hidden', false);
    list.classList.toggle('hidden', true);
    btnGallery.classList.toggle('active', true)
    btnList.classList.toggle('active', false)
});
// Add a click event listener to the button
btnList.addEventListener('click', function() {
    // Toggle the 'hidden' class on both elements
    gallery.classList.toggle('hidden', true);
    list.classList.toggle('hidden', false);
    btnList.classList.toggle('active', true)
    btnGallery.classList.toggle('active', false)
});
</script>