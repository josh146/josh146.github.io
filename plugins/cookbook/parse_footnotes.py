from bs4 import BeautifulSoup


def parse_footnotes(article):
    if "[ref]" not in article._content:
        return

    content = article._content.replace("[ref]", "<footnote>").replace("[/ref]", "</footnote>")
    soup = BeautifulSoup(content, "html5lib")

    footnotes = []

    # process footnotes
    for i, tag in enumerate(soup.find_all("footnote"), 1):
        # Skip if inside a code block
        if tag.find_parent("code"):
            continue

        fn_id = f"sf-{article.slug}-{i}"
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

            back_link = soup.new_tag("a", href=f"#{back_id}", **{"class": "simple-footnote-back"})
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
    article._content = output.replace("<footnote>", "").replace("</footnote>", "")
