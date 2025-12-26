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
        self.parse_footnotes()
        self.parse_timeline()

        soup = BeautifulSoup(self._content, "html.parser")

        # Initialize sections
        self.intro_html = ""
        self.ingredients_html = ""
        self.method_html = ""
        self.notes_html = ""
        self.footnotes_html = ""  # Store footnotes here

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

        footnotes = []

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
            footnotes.append((tag.extract(), fn_id, back_id))

        # build the Footer List
        if footnotes:
            ol = soup.new_tag("ol", **{"class": "simple-footnotes"})

            for fn_content, fn_id, back_id in footnotes:
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
        output = str(soup)
        output = output.replace("<html><head></head><body>", "").replace("</body></html>", "")

        # Revert any ignored footnotes back to brackets
        self._content = output.replace("<footnote>", "").replace("</footnote>", "")


class RecipePostProcessor:

    def __init__(self, recipes, recipes_index):
        self.recipes = recipes
        self.recipes_index = recipes_index

        for recipe in self.recipes:
            self.inject_components(recipe)

        for recipe in self.recipes:
            self.parse_wikilinks(recipe)

    def inject_components(self, recipe):
        """
        Scans HTML for [[Component: title]]. If found, replaces it in-place.
        """
        # Regex to find [[Component: title]], optionally wrapped in <p> tags by Markdown
        # Capture groups: 1=Opening <p>, 2=title, 3=Closing </p>
        # tag_pattern = re.compile(r"(<p>\s*)?\[\[Component: (.*?)\]\](\s*<\/p>)?", re.IGNORECASE)
        tag_pattern = re.compile(r'(<p>\s*)?\[\[Component: (.*?)(?:\s*\|\s*([\w\s-]+))?\]\](\s*<\/p>)?', re.IGNORECASE)
        tag_pattern = re.compile(r'(<p>\s*)?\[\[Component: (.*?)(?:\s*\|\s*(.*?))?\]\](\s*<\/p>)?', re.IGNORECASE)

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
                        raw_args = match.group(3) # "section | 0.5" or "0.5" or None

                        # parse Arguments
                        section_target = None
                        scale_factor = 1.0

                        if raw_args:
                            clean_args = re.sub(r'<[^>]+>', '', raw_args)
                            parts = [p.strip() for p in clean_args.split('|')]
                            for p in parts:
                                # Check if it looks like a number
                                try:
                                    scale_factor = float(p)
                                except ValueError:
                                    # If not a number, it must be the section name
                                    section_target = p

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

                                        return f"<h3>{header.get_text()}</h3>\n{str(next_list)}"

                            # Fallback: specific section not found
                            print(f"Warning: Section '{section_target}' not found in component '{title}'")

                        placed_components.add(title)
                        # Decide if we are inserting Ingredients or Method based on attribute

                        if "ingredients" in section_attr:
                            content = RecipePostProcessor.scale_quantities(component_recipe.ingredients_html, scale_factor)
                        else:
                            content = component_recipe.method_html

                        # Return the HTML with a Header
                        return f"<h3>{component_recipe.title}</h3>\n{content}"

                    return ""  # If component not found, remove the tag

                # Perform the substitution
                current_html = tag_pattern.sub(replace_match, current_html)
                setattr(recipe, section_attr, current_html)

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
            url = f"/{self.recipes_index.get(fix_string(key.lower())).url}"

            if url:
                # Success: Return the styled link
                return f'<a href="{url}" class="component-link">{display_text}</a>'
            else:
                # Fallback: Recipe not found? Just return the text without [[ ]]
                print(f"⚠️ Warning: Could not find recipe link for [[{key}]] in {recipe.title}")
                return display_text

        recipe.ingredients_html = pattern.sub(replace_match, recipe.ingredients_html)
        recipe.method_html = pattern.sub(replace_match, recipe.method_html)
        recipe.intro_html = pattern.sub(replace_match, recipe.intro_html)
        recipe.notes_html = pattern.sub(replace_match, recipe.notes_html)
