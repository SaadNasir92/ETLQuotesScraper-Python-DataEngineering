# Weekend challenge: go through first 10 pages, extract the text, author, tags. 
# Imports
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

def perform_scrape(website: str, num_pages: int) -> str:
    """
    Perform web scraping on the given website for a specified number of pages.

    Args:
        website (str): The URL of the website to scrape.
        num_pages (int): The number of pages to scrape.

    Returns:
        str: The path to the CSV file containing the scraped data.
    """
    
    browser = make_browser()
    all_data = scrape_web(browser, website, num_pages)
    file = make_csv(all_data)
    close_browser(browser)
    print(f'Scraped {num_pages} pages from {website}.')
    return file

def make_browser():
    """
    Create and configure a new browser instance.

    Returns:
        Browser: An instance of the Splinter Browser object configured with Chrome.
    """
    
    browser_obj = Browser(driver_name='chrome')
    return browser_obj
    
def close_browser(chrome_obj):
    """
    Close the given browser instance.

    Args:
        chrome_obj (Browser): The browser instance to close.
    """
    chrome_obj.quit()

def scrape_web(chrome_obj, website: str, num_pages: int) -> list:
    """
    Scrape multiple pages from the specified website using the provided browser instance.

    Args:
        chrome_obj (Browser): The browser instance to use for scraping.
        website (str): The URL of the website to scrape.
        num_pages (int): The number of pages to scrape.

    Returns:
        list: A list of dictionaries containing the scraped data from all pages.
    """
    
    chrome_obj.visit(website)
    
    complete_page_data = []
    
    for page_num in range(num_pages):
        current_pg_html = chrome_obj.html
        complete_page_data.extend(parse_page(current_pg_html, page_num))
        go_next_page(chrome_obj)
        
    return complete_page_data

def parse_page(html_code: str, page_num: int) -> list:
    """
    Parse all quotes on a given HTML page.

    Args:
        html_code (str): The HTML code of the page to parse.
        page_num (int): The current page number being parsed.

    Returns:
        list: A list of dictionaries, each containing an author, quote, and tag.
    """
    soup = BeautifulSoup(html_code, 'html.parser')
    
    # Gather all quotes in a list from current page
    page_quotes = [x for x in soup.select('div.quote')]
    
    page_data = []
    
    # Grab current quote, author and tags
    for each_quote in page_quotes:
        quote = each_quote.select('span.text')[0].text
        author = each_quote.select('span small.author')[0].text
        tags = each_quote.select('div.tags a')
        if len(tags) == 0:
            page_data.append({'author': author, 'quote': quote, 'tag': 'no_tag_found'})
        else:
            # Loop through tags to make a separate dictionary entry for each tag
            for tag in tags:
                page_data.append({'author': author, 'quote': quote, 'tag': tag.text})
    
    log_data(page_data, page_num)
    # return the list of dictionaries for the page        
    return page_data

def go_next_page(chrome_obj):
    """
    Navigate to the next page of the website using the provided browser instance.

    Args:
        chrome_obj (Browser): The browser instance to use for navigation.
    """
    next_button = chrome_obj.links.find_by_partial_text("Next")
    if len(next_button) > 0:
        next_button.links.find_by_partial_text("Next").click()
    
def log_data(data: list, page_num: int):
    """
    Log the number of quotes parsed from the current page to a log file.

    Args:
        data (list): The list of dictionaries containing the parsed data.
        page_num (int): The current page number.
    """
    log_number_parsed = len(data)
    with open('resources/log.txt', 'a') as file:
        file.write(f'Parsed {log_number_parsed} quotes on page number {page_num + 1}.\n')

def make_csv(data: list) -> str:
    """
    Create a CSV file from the provided data using pandas library.

    Args:
        data (list): The list of dictionaries containing the scraped data.

    Returns:
        str: The path to the created CSV file.
    """
    csv_path = 'resources/scraped_data.csv'
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    return csv_path