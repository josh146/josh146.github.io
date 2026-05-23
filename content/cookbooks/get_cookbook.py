import regex as re
import argparse
import sys
import requests
from bs4 import BeautifulSoup
import time
import yaml

def get_recipes(url):

    # Paste your copied cookie string here
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': 'ASP.NET_SessionId=3bdzb1olpeavqr00yv4qfrwx; cf_clearance=Qz4Mz.OBLoNm3ScT3PD7t.nEehcjajq5c7KYGaHcagQ-1779565413-1.2.1.1-.ZDy9LkGH9OdUIx7HrjXyvTsmJDGWGGI.oo_zX47j9OL6DhFid337WACleuw9.BXpUu5tSSHBnB8GzQzRlcYSL18l_hqx4QeJuGFHu8qz2U5Vl8iajF3aRflyiMVYS32BLls2nUKdAL_ZT9_LbiCSCQCFylqnCtDQV6fhqvhlFUsmFOnQjcNDybdoSDTFCUeCGX.IbOBag1wlCBszOdWo4UBF4XLF5dHZeevidZnsip.i5P8hlTwtpmppaXuWunlA1o0vcHiQFK_P0wfTsJLjpIK1FJB4alZFq7qLdXQGdCD0ajtl81QjYuh08Twm.VdCdMMIo6aTtCfX7UHoYilXg; ajs_anonymous_id=f479f391-449a-460c-a7aa-6e040de94f96; _fbp=fb.1.1777753584918.623933169432554548; _ga_BJ06C571TF=GS2.1.s1779565413$o14$g1$t1779565428$j45$l0$h0; _ga=GA1.1.210282990.1777753585; EYBLogonCookie=B93C97DC885F35242562D0AB334CD51373BB2DA0550A213AC0AB2E7C4BE5BB81863238D7DE151509DDAF180E1C46D8312D84E2595A420EAB72B41C06CD6BD6923D20D06895D825428F62F62B8017424F3F548C1B; ajs_user_id=709202; eatyourbooks_new_visitor=; .ASPXROLES=mklMI9lTMKHblJqT3jMotS1TvL1E7-2V45BoB_3q_EcYi9BwlDjwtyo3lvnLkjOl91P3oHUJVvQfXapMrGMXu1-td0CKe_ZOl2Fowv0uss9FtNS7djLJfnpAo9xzw0dANGmTeE-iEzpTSTEJbEHYB_4favHXjqf5uCADlXrq5Z4-WExsa5zG126TioFX3WWU1oe-65iSLoOOnFsXF705Zx7_86VyRgIDXNNX7jVIxDOG73BvlhNxlIEOsJtlvgmuPigSnkgb3Wi8tF6fBrWytrj1hoZZbfxbQvoOD0_JXv539WaVfichCLsVx5IyonpOdx8CrqAr8zEuYokYT44Jt94hJ47NF70-Ps_U68GAcZLSDLWG5JrlylvEBqPJ1V45kqC3fMyjSNBRjEBGKYyJVK3VmL7YU1JFxUd66bFnFF4X9G-Uk2Y2Xf_3ySVFCHYw0TItVDNatKh4J7Z4bjXGv-q17S01; ph_phc_BsWMSq1CjtFSX5BwgpxJfMIh232b8yr4OdF4CLsHbyB_posthog=%7B%22%24device_id%22%3A%22019dea5e-f43e-7741-94fd-9f48f382bf59%22%2C%22distinct_id%22%3A%22FPsxw61RJnRU1inXGkRQTjs7okf1%22%2C%22%24sesid%22%3A%5B1779565594937%2C%22019e565d-4774-7244-b0b5-098d11110516%22%2C1779565414253%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22u%22%3A%22https%3A%2F%2Fwww.eatyourbooks.com%2Flibrary%2F202540%2Frambutan-fresh-sri-lankan-recipes%22%7D%2C%22%24user_state%22%3A%22identified%22%7D'
    }

    # The request will now act as if it is already logged in!
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    book_title = soup.find('h1').find(string=True).strip()
    authors = [tag.get_text() for tag in soup.select('h1 a', class_='author')]
    cover = soup.select('.book-cover img')[0]['src']

    # Example: Find the recipe titles (You will need to inspect EYB's HTML to get the exact class names)
    titles = [tag.get_text() for tag in soup.find_all('a', class_='RecipeTitleExp')]
    pages = [re.sub(r'\(page (\d+)\)', r'\1', tag.get_text()) for tag in soup.find_all('i', class_='PageNoExp')]
    ingredients = [[re.sub(r'^ ', '', r) for r in tag.next_sibling.strip().split(';')] for tag in soup.find_all("b", string=re.compile("Ingredients:"))]

    if pages:
        formatted_recipes = [
            {
                'title': item[0],
                'page': int(item[1]),  # Converts the page string to an integer
                'ingredients': item[2]
            }
            for item in zip(titles, pages, ingredients)
        ]
    else:
        formatted_recipes = [
            {
                'title': item[0],
                'ingredients': item[1]
            }
            for item in zip(titles, ingredients)
        ]

    return {
        "book": book_title,
        "author": ", ".join(authors),
        "cover": cover
    }, formatted_recipes


def get_all_recipes(url):
    recipes = []
    page = 1

    while True:
        print(f"Getting recipes from page {page}...")
        book_info, r = get_recipes(f"{url}/{page}")

        if not r:
            print("No more recipes found. Scraping complete!")
            break

        recipes += r
        page += 1
        time.sleep(2)

    return book_info | {'recipes': recipes}

def generate_recipe_yaml(recipes):
    # Start the YAML string with the root key
    yaml_lines = ["recipes:"]

    for recipe in recipes:
        # Unpack the tuple
        title, page, ingredients = recipe

        # Build the YAML block for this recipe
        yaml_lines.append(f"  - title: {title}")
        yaml_lines.append(f"    page: {page}")

        # Python's default string representation of a list looks exactly
        # like a YAML flow-style array!
        yaml_lines.append(f"    ingredients: {ingredients}")

    # Join everything together with line breaks
    return "\n".join(yaml_lines)


def format_recipes(text):
    # --- RULE 1: Replace specific patterns with nothing ---
    text = re.sub(r'^ +\d\n +Recipe Online\n + Report Broken Link', '', text, flags=re.MULTILINE)
    text = re.sub(r'^ +Accompaniments.+\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^ +Categories:.+\n +', '', text, flags=re.MULTILINE)
    text = re.sub(r'^ *\d\n', '', text, flags=re.MULTILINE)

    # --- RULE 2: Extract title and page ---
    pattern_2 = r'^ +([A-Za-z ,\'\-:é&!áö"èùêàâ\(\)%\[\]\']+) \(page ([0-9]+)\)'
    replace_2 = r'  - title: "\1"\n    page: \2'
    text = re.sub(pattern_2, replace_2, text, flags=re.MULTILINE)

    # --- RULE 3: Wrap ingredients in quotes ---
    pattern_3 = r'(?:\bIngredients:\s*|(?!\A)\G;\s*)\K([^;\n]+)'
    replace_3 = r'"\1"'
    text = re.sub(pattern_3, replace_3, text)

    # --- RULE 4: Wrap the ingredients line in an array ---
    pattern_4 = r'^Ingredients:\s*(.*)$'
    replace_4 = r'    ingredients: [\1]'
    text = re.sub(pattern_4, replace_4, text, flags=re.MULTILINE)

    # --- RULE 5: Remove specific text preceding the title ---
    pattern_5 = r'([A-Za-z ,\'\-:é&!áö"èùê\(\)]+\n)^  - title'
    replace_5 = r'  - title'
    text = re.sub(pattern_5, replace_5, text, flags=re.MULTILINE)

    return text

if __name__ == "__main__":
    # 1. Set up the argument parser
    parser = argparse.ArgumentParser(description="Clean and format recipe text files into YAML.")

    # 2. Define the positional arguments
    parser.add_argument("url", help="URL for the recipe index")
    parser.add_argument("output", help="Path where the formatted file will be saved.")
    parser.add_argument("--wishlist", action="store_true", help="Store the cookbook under wishlist.")

    # 3. Parse the arguments provided by the user
    args = parser.parse_args()

    try:
        recipes = get_all_recipes(args.url)

        if args.wishlist:
            recipes["wishlist"] = True

        with open(args.output, 'w') as file:
            yaml.dump(recipes, file, sort_keys=False)

        # processed_text = format_recipes(raw_text)

        # with open(args.output, 'w', encoding='utf-8') as f:
        #     f.write(processed_text)

        # print(f"Success! Processed recipes saved to {args.output}")

    except FileNotFoundError:
        print(f"Error: Could not find '{args.input}'. Please ensure the file exists.")
