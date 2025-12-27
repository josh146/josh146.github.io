import markdown
from bs4 import BeautifulSoup
import re
from pelican.contents import Page


def fix_string(s):
    s = s.replace("&nbsp;", " ")
    s = s.replace("\u00a0", " ")
    s = s.replace("&#8220;", "'")
    s = s.replace("&#8221;", "'")
    s = s.replace("&#8216;", "'")
    s = s.replace("&#8217;", "'")
    return s


class Recipe(Page):
    """
    A custom content object for Recipes.
    """

    default_template = "recipe"

    SECTION_MAP = {
        "ingredients": "ingredients_html",
        "method": "method_html",
        "steps": "method_html",
        "instructions": "method_html",  # Handle synonyms
        "notes": "notes_html",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process()

    def process(self):
        """
        Splits the content into intro, ingredients, method, and notes.
        Stores them as attributes on the recipe object.
        """
        self.title = fix_string(self.title)

        self.footnotes = []  # Store footnotes here
        self.footnotes_html = ""
        self.parse_footnotes()
        self.build_footnotes()

        self.parse_timeline()

        soup = BeautifulSoup(self._content, "html.parser")

        # Initialize sections
        self.intro_html = ""
        self.ingredients_html = ""
        self.method_html = ""
        self.notes_html = ""

        # Initialize raw lists for Schema
        self.ingredients_list = []
        self.instructions_list = []

        # Standardize headers to look for (lowercase for comparison)
        current_section = "intro_html"

        # Iterate over all top-level elements
        for tag in soup:
            # Get safe tag name
            tag_name = getattr(tag, "name", None)

            # check for Section Headers
            if tag_name == "h2":
                header_text = tag.get_text().strip().lower().rstrip(":")
                if header_text in Recipe.SECTION_MAP:
                    current_section = Recipe.SECTION_MAP[header_text]
                    continue

            # Append the tag to the current section string
            # We convert the tag back to string to preserve HTML
            setattr(self, current_section, getattr(self, current_section) + str(tag))

        if self.ingredients_html:
            self._parse_ingredients()

        if self.method_html:
            self._parse_method()

        if hasattr(self, "servings"):
            self.servings_html = Recipe._apply_scaling_to_html(self.servings)

    def _parse_ingredients(self):
        ing_soup = BeautifulSoup(self.ingredients_html, "html.parser")
        self.ingredients_list = [li.get_text().strip() for li in ing_soup.find_all("li")]
        self.ingredients_html = Recipe._apply_scaling_to_html(self.ingredients_html)
        self.ingredients_html = re.sub(
            r"(\([^)]+\))", r'<span class="paren">\1</span>', self.ingredients_html
        )

    def _parse_method(self):
        method_soup = BeautifulSoup(self.method_html, "html.parser")

        steps = method_soup.find_all("li")

        if not steps:
            # Fallback: If the user didn't use a list, look for paragraphs
            steps = method_soup.find_all("p")

        self.instructions_list = [s.get_text().strip() for s in steps]

        # Clean up empty strings just in case
        self.instructions_list = [i for i in self.instructions_list if i]

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
        days = re.search(r"(\d+)\s*d", duration_str)
        if days:
            d = int(days.group(1))
            total_mins += d * 24 * 60

            if d == 1:
                label += f"{d} day "
            else:
                label += f"{d} days "

        # Check for Hours
        hours = re.search(r"(\d+)\s*h", duration_str)
        if hours:
            h = int(hours.group(1))
            total_mins += h * 60

            if h == 1:
                label += f"{h} hour "
            else:
                label += f"{h} hours "

        # Check for Minutes
        mins = re.search(r"(\d+)\s*m", duration_str)
        if mins:
            m = int(mins.group(1))
            total_mins += m
            label += f"{m} min"

        return total_mins, label

    def parse_timeline(self):
        if not hasattr(self, "timeline"):
            return

        # We convert it into a list of dictionaries.
        parsed_timeline = []
        current_offset = 0

        # Split into individual steps
        timeline_str = self.timeline
        steps = timeline_str.split(";")

        for item in steps:
            # Skip empty items (e.g. if there is a trailing semicolon)
            if not item.strip():
                continue

            try:
                # Expected format: "Task | Duration | Type"
                parts = [p.strip() for p in item.split("|")]

                task_name = parts[0]

                duration_str = parts[1]
                duration_mins, label = Recipe._parse_duration_string(duration_str)

                # Default to 'active' if type is missing
                step_type = parts[2].lower() if len(parts) > 2 else "active"

                parsed_timeline.append(
                    {
                        "task": task_name,
                        "duration": duration_mins,
                        "duration_display": label,  # Keep original text for display
                        "type": step_type,
                        "start_offset": current_offset,
                        "end_offset": current_offset + duration_mins,
                    }
                )

                current_offset += duration_mins

            except Exception as e:
                print(f"Error parsing timeline item '{item}': {e}")

        self.timeline_parsed = parsed_timeline
        self.total_duration_mins = current_offset

    @staticmethod
    def _apply_scaling_to_html(html_content):
        """
        Parses HTML, finds numbers in text nodes, and wraps them in spans.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        number_pattern = re.compile(r"(?<!\w)(\d+(?:[./]\d+)?)")

        for text_node in soup.find_all(string=True):
            # Skip numbers inside links, existing spans, or scripts
            if text_node.parent.name in ["a", "script", "style", "sup"]:
                continue

            # If we find a number, replace it
            if number_pattern.search(text_node):
                new_html = number_pattern.sub(
                    lambda m: Recipe._make_scalable_span(m.group(0)), text_node
                )
                # Replace the text node with the new HTML structure
                text_node.replace_with(BeautifulSoup(new_html, "html.parser"))

        return str(soup)

    @staticmethod
    def _make_scalable_span(val_str):
        """Helper to create the HTML for the scalable number"""
        try:
            if "/" in val_str:
                num, den = val_str.split("/")
                base_val = float(num) / float(den)
            else:
                base_val = float(val_str)
            return f'<span class="scalable" data-base="{base_val}">{val_str}</span>'
        except ValueError:
            return val_str

    def parse_footnotes(self):
        if "[ref]" not in self._content:
            return

        content = self._content.replace("[ref]", "<footnote>").replace("[/ref]", "</footnote>")
        soup = BeautifulSoup(content, "html5lib")

        # process footnotes
        for i, tag in enumerate(soup.find_all("footnote"), 1):
            # Skip if inside a code block
            if tag.find_parent("code"):
                continue

            fn_id = f"sf-{self.slug}-{i}"
            back_id = f"{fn_id}-back"

            # Create the superscript number: <sup><a ...>1</a></sup>
            sup = soup.new_tag("sup", id=back_id)
            link = soup.new_tag("a", href=f"#{fn_id}", **{"class": "simple-footnote"})
            link.string = str(i)
            link["title"] = tag.get_text(strip=True)
            sup.append(link)

            # Insert superscript before the footnote, then remove the footnote content
            tag.insert_before(sup)

            # Extract the tag to move it to the footer later
            self.footnotes.append((tag.extract(), fn_id, back_id))

        # Remove the wrapper tags
        output = str(soup)
        output = output.replace("<html><head></head><body>", "").replace("</body></html>", "")

        # Revert any ignored footnotes back to brackets
        self._content = output.replace("<footnote>", "").replace("</footnote>", "")

    def build_footnotes(self):
        if not self.footnotes:
            return

        soup = BeautifulSoup("", "html.parser")
        ol = soup.new_tag("ol", **{"class": "simple-footnotes"})

        for fn_content, fn_id, back_id in self.footnotes:
            li = soup.new_tag("li", id=fn_id)

            # Move the inner HTML of the footnote to the list item
            # .contents is a list of children; we append them to the new li
            li.append(fn_content)

            back_link = soup.new_tag(
                "a", href=f"#{back_id}", **{"class": "simple-footnote-back"}
            )
            back_link.string = "\u21a9\ufe0e"

            li.append(" ")
            li.append(back_link)
            ol.append(li)

        # Append list to the body (or end of document)
        if soup.body:
            soup.body.append(ol)
        else:
            soup.append(ol)

        # Remove the wrapper tags
        self.footnotes_html = str(soup)


class RecipePostProcessor:

    def __init__(self, recipes, recipes_index):
        self.recipes = recipes
        self.recipes_index = recipes_index

        for recipe in self.recipes:
            self.inject_components(recipe)

        for recipe in self.recipes:
            self.parse_wikilinks(recipe)
            recipe.related = self.related_recipes(recipe, limit=3)

    def inject_components(self, recipe):
        """
        Scans HTML for [[Component: title]]. If found, replaces it in-place.
        """
        tag_pattern = re.compile(r'(<p>\s*)?\[\[Component: (.*?)(?:\s*\|\s*(.*?))?\]\](\s*<\/p>)?', re.IGNORECASE)

        # A set to track which components we've added footnotes for
        # (so we don't add the same footer twice if included twice)
        added_footnotes = set()

        # process Ingredients and Method separately
        for section_attr in ["ingredients_html", "method_html"]:
            if not hasattr(recipe, section_attr):
                return

            current_html = getattr(recipe, section_attr)

            # Search for tags in the current HTML
            matches = tag_pattern.findall(current_html)

            # Identify which components were manually placed
            placed_components = set()

            if matches:
                # We need to rebuild the string with replacements
                # We use a callback function for re.sub to handle the logic

                recipe.components = []

                def replace_match(match):
                    # match.group(2) is the title (e.g., 'swiss-meringue')
                    title = fix_string(match.group(2))

                    try:
                        component_recipe = self.recipes_index[title.lower()]
                    except:
                        print(
                            f"⚠️ Warning: Could not find link for [[Component: {title}]] in {recipe.title}"
                        )
                        return ""

                    if component_recipe:
                        recipe.components.append(component_recipe)
                        raw_args = match.group(3) # "section | 0.5" or "0.5" or None

                        # parse Arguments
                        section_target = None
                        scale_factor = 1.0
                        show_header = True  # Default is True

                        if raw_args:
                            clean_args = re.sub(r'<[^>]+>', '', raw_args)
                            parts = [p.strip() for p in clean_args.split('|')]
                            for p in parts:
                                if p.lower() in ['no_header', 'headless', 'no-title']:
                                    show_header = False
                                    continue # Skip to next part

                                # Check if it looks like a number
                                try:
                                    scale_factor = float(p)
                                except ValueError:
                                    # If not a number, it must be the section name
                                    section_target = p

                        if component_recipe.footnotes:
                            if title not in added_footnotes:
                                # Append this component's footnotes to the main article
                                # We strip the outer <div class="footnote"> wrapper to avoid nesting divs,
                                # or just stack them. Stacking is safer/easier.
                                recipe.footnotes += component_recipe.footnotes
                                recipe.build_footnotes()
                                added_footnotes.add(title)

                        if section_target is not None:
                            soup = BeautifulSoup(getattr(component_recipe, section_attr), 'html.parser')
                            target_clean = section_target.lower().strip()

                            # Find headers (h3 or h4)
                            for header in soup.find_all(['h3', 'h4']):
                                if header.get_text().strip().lower() == target_clean:
                                    # Found the header! Now grab the list immediately following it
                                    # We look for the next sibling that is a list
                                    next_list = header.find_next_sibling(['ul', 'ol'])

                                    if next_list:
                                        # apply scaling (ONLY to ingredients)
                                        if 'ingredients' in section_attr:
                                            next_list = RecipePostProcessor.scale_quantities(str(next_list), scale_factor)

                                        if show_header:
                                            return f"<h3>{header.get_text()}</h3>\n{str(next_list)}"

                                        return f"{str(next_list)}"

                            # Fallback: specific section not found
                            print(f"Warning: Section '{section_target}' not found in component '{title}'")

                        placed_components.add(title)
                        # Decide if we are inserting Ingredients or Method based on attribute

                        if "ingredients" in section_attr:
                            content = RecipePostProcessor.scale_quantities(component_recipe.ingredients_html, scale_factor)
                        else:
                            content = component_recipe.method_html

                        if show_header:
                            return f"<h3>{component_recipe.title}</h3>\n{content}"

                        return f"{content}"

                    return ""  # If component not found, remove the tag

                # Perform the substitution
                current_html = tag_pattern.sub(replace_match, current_html)
                setattr(recipe, section_attr, current_html)

                if added_footnotes:
                    self.rebuild_footnotes(recipe)

    @staticmethod
    def rebuild_footnotes(recipe):
        """
        Parses ingredients, method, and footnotes to ensure they are
        numbered sequentially (1, 2, 3...) across the entire unified page.
        """
        # We parse all three sections because references can appear in ingredients OR method
        soup_ing = BeautifulSoup(recipe.ingredients_html, 'html.parser')
        soup_met = BeautifulSoup(recipe.method_html, 'html.parser')

        # If there are no footnotes at all, skip
        if not recipe.footnotes:
            return

        soup_notes = BeautifulSoup(recipe.footnotes_html, 'html.parser')

        # 2. The State Machine
        new_id_counter = 1
        id_map = {} # Maps 'fn:lamb-1' -> 1

        # Helper to process a soup and update references
        def process_refs(soup):
            nonlocal new_id_counter
            # Python-Markdown generates <sup id="fnref:slug-1"><a href="#fn:slug-1">...</a></sup>
            # We look for the <a> tag
            for link in soup.find_all('a', class_='simple-footnote'):
                old_href = link.get('href') # e.g. "#fn:lamb-1"
                old_id_key = old_href.replace('#', '') # "fn:lamb-1"

                # Have we seen this footnote before?
                if old_id_key not in id_map:
                    id_map[old_id_key] = new_id_counter
                    new_id_counter += 1

                # Get the new number
                new_num = id_map[old_id_key]

                # UPDATE THE HTML IN-PLACE
                # 1. Update text: [1]
                link.string = f"{new_num}"
                # 2. Update href: #fn:1
                link['href'] = f"#fn:{new_num}"
                # 3. Update the parent <sup> id: fnref:1
                parent_sup = link.find_parent('sup')
                if parent_sup:
                    parent_sup['id'] = f"fnref:{new_num}"

        # 3. Run the scan in reading order
        process_refs(soup_ing)
        process_refs(soup_met)

        # 4. Rebuild the Definitions List
        # The definitions are currently in a random order or grouped by component.
        # We need to pick them out and sort them by our new IDs.

        new_ol = soup_notes.new_tag('ol')
        new_ol["class"] = "simple-footnotes"
        original_li_elements = {li['id']: li for li in soup_notes.find_all('li', id=True)}

        # Iterate 1..N to build the new list in order
        # We invert the map to go Number -> Old ID
        # (Note: id_map keys are 'fn:old-id', values are Integers)
        sorted_map = sorted(id_map.items(), key=lambda item: item[1])

        for old_key, new_num in sorted_map:
            # Find the original <li> definition
            if old_key in original_li_elements:
                li = original_li_elements[old_key]

                # UPDATE THE DEFINITION HTML
                # 1. Update list item ID: id="fn:1"
                li['id'] = f"fn:{new_num}"

                # 2. Update the Back Link (↩)
                # Python-Markdown uses class="footnote-backref"
                backlink = li.find('a', class_='simple-footnote-back')
                if backlink:
                    backlink['href'] = f"#fnref:{new_num}"

                # Append to our new ordered list
                new_ol.append(li)

        # 5. Commit Changes back to Article
        # Replace the old list with the new sorted one
        old_ol = soup_notes.find('ol', class_='simple-footnotes')
        if old_ol:
            old_ol.replace_with(new_ol)

        recipe.ingredients_html = str(soup_ing)
        recipe.method_html = str(soup_met)
        recipe.footnotes_html = str(soup_notes)

    @staticmethod
    def scale_quantities(html_fragment, scale_factor):
        """
        Multiplies numbers found in <span class="scalable">...</span> by the scale factor.
        """
        if scale_factor == 1.0:
            return html_fragment

        def math_replacer(match):
            original_number = match.group(1)
            try:
                # Handle fractions like "1/2" or ranges "1-2" if you want to get fancy
                # For now, let's handle standard floats/ints
                val = float(original_number)
                new_val = val * scale_factor

                # Formatting: remove trailing zeros (250.0 -> 250)
                formatted = "{:.2f}".format(new_val).rstrip('0').rstrip('.')
                return f'<span class="scalable" data-base="{formatted}">{formatted}</span>'
            except ValueError:
                # If it's not a number (e.g. "some"), leave it alone
                return f'<span class="scalable" data-base="{formatted}>{original_number}</span>'

        # Regex finds: <span class="scalable">123</span>
        pattern = re.compile(r'<span class="scalable" data-base="[\d\.]+">([\d\.]+)</span>')
        return pattern.sub(math_replacer, html_fragment)

    def parse_wikilinks(self, recipe):
        """
        regex replace [[Link]] with <a class="component-link">...</a>
        """
        # Regex breakdown:
        # \[\[       Match opening [[
        # (.*?)      Group 1: The 'Key' (Recipe Title) - non-greedy
        # (?:\|(.*?))? Group 2: Optional 'Display Text' (after |)
        # \]\]       Match closing ]]
        pattern = re.compile(r"\[\[(.*?)(?:\|(.*?))?\]\]")

        def replace_match(match):
            key = match.group(1).strip()
            display_text = match.group(2).strip() if match.group(2) else key

            # Lookup URL using lowercase key
            linked_recipe = self.recipes_index.get(fix_string(key.lower()))

            if linked_recipe is not None:
                # Success: Return the styled link
                url = f"/{linked_recipe.url}"
                return f'<a href="{url}" class="component-link">{display_text}</a>'
            else:
                # Fallback: Recipe not found? Just return the text without [[ ]]
                print(f"⚠️ Warning: Could not find recipe link for [[{key}]] in {recipe.title}")
                return display_text

        recipe.ingredients_html = pattern.sub(replace_match, recipe.ingredients_html)
        recipe.method_html = pattern.sub(replace_match, recipe.method_html)
        recipe.intro_html = pattern.sub(replace_match, recipe.intro_html)
        recipe.notes_html = pattern.sub(replace_match, recipe.notes_html)

    def related_recipes(self, recipe, limit=3):
        """
        Finds related recipes based on weighted scoring of Title, Category, and Tags.
        Weights: Title Match (3), Category Match (2), Tag Match (1)
        """
        current_tags = set(getattr(recipe, "tags", []))

        # Title Keywords (Clean up common words)
        ignore_words = {'the', 'a', 'an', 'and', 'with', 'recipe', 'how', 'to', 'make', 'easy', 'best'}
        current_title_words = set(re.findall(r'\w+', recipe.title.lower())) - ignore_words

        scored_recipes = []

        for r in self.recipes:
            # Skip self
            if r is recipe:
                continue

            score = 0

            # category match (+2 points)
            if r.category == recipe.category:
                score += 2

            # tag overlap (+1 point each)
            other_tags = set(getattr(r, "tags", []))
            score += len(current_tags.intersection(other_tags))

            # title word overlap (+3 points each)
            other_title_words = set(re.findall(r'\w+', r.title.lower())) - ignore_words
            title_matches = len(current_title_words.intersection(other_title_words))
            score += (title_matches * 3)

            if score > 0:
                scored_recipes.append((score, r))

        # Sort by score descending
        scored_recipes.sort(key=lambda x: x[0], reverse=True)

        return [item[1] for item in scored_recipes[:limit]]
