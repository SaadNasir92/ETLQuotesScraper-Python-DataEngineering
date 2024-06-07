# Weekend challenge: go through first 10 pages, extract the text, author, tags. 
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import re
# Imports and setup
browser = Browser(driver_name='chrome')
url = "http://quotes.toscrape.com/"
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# Function to parse all quotes on a page. Returns 
def parse_page():
    """
    Parses the current web page to extract quotes, authors, and tags.

    This function searches the HTML of the current page for elements that contain quotes,
    their authors, and associated tags. It expects the HTML structure to contain:
    - Quotes within <span class="text"> elements inside <div class="quote"> elements.
    - Authors within <small class="author"> elements inside <div class="quote"> elements.
    - Tags within <a> elements inside <div class="tags"> elements within <div class="quote"> elements.

    The function extracts this data and compiles it into a list of dictionaries,
    where each dictionary represents a quote with its corresponding author and tag.

    Returns:
        list of dict: A list of dictionaries, where each dictionary contains the keys 'author', 'quote',
        and 'tag', representing the respective data extracted from the page.

    Example:
        >>> data = parse_page()
        >>> print(data)
        [{'author': 'Author 1', 'quote': 'Quote 1', 'tag': 'tag1'}, {'author': 'Author 1', 'quote': 'Quote 1', 'tag': 'tag2'}, ...]

    Raises:
        IndexError: If the expected elements (e.g., span.text, small.author) are not found within each quote.
        This can occur if the structure of the HTML does not match the expected pattern.
    """
    # Gather all quotes in a list from current page
    page_quotes = [x for x in soup.select('div.quote')]
    
    page_data = []
    
    # Grab current quote, author and tags
    for each_quote in page_quotes:
        quote = each_quote.select('span.text')[0].text
        author = each_quote.select('span small.author')[0].text
        tags = each_quote.select('div.tags a')
        
        # Loop through tags to make a separate dictionary entry for each tag
        for tag in tags:
            page_data.append({'author': author, 'quote': quote, 'tag': tag.text})
            
    # return the list of dictionaries for the page        
    return page_quotes