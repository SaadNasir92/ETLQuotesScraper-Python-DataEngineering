# Weekend challenge: go through first 10 pages, extract the text, author, tags. 
# Imports
from bs4 import BeautifulSoup
from splinter import Browser
import numpy as np
import pandas as pd

def perform_scrape(website, num_pages):
    browser = make_browser()
    all_data = scrape_web(browser, website, num_pages)
    file = make_csv(all_data)
    close_browser(browser)
    print(f'Scraped {num_pages} pages from {website}.')
    return file

def make_browser():
    browser_obj = Browser(driver_name='chrome')
    return browser_obj
    
def close_browser(chrome_obj):
    chrome_obj.quit()

# Function to scrape multiple pages
def scrape_web(chrome_obj, website, num_pages):
    
    chrome_obj.visit(website)
    
    complete_page_data = []
    
    for page_num in range(num_pages):
        current_pg_html = chrome_obj.html
        complete_page_data.extend(parse_page(current_pg_html, page_num))
        go_next_page(chrome_obj)
        
    return complete_page_data

# Function to parse all quotes on a page. Returns 
def parse_page(html_code, page_num):
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
            page_data.append({'author': author, 'quote': quote, 'tag': np.nan})
        else:
            # Loop through tags to make a separate dictionary entry for each tag
            for tag in tags:
                page_data.append({'author': author, 'quote': quote, 'tag': tag.text})
    
    log_data(page_data, page_num)
    # return the list of dictionaries for the page        
    return page_data

def go_next_page(chrome_obj):
    next_button = chrome_obj.links.find_by_partial_text("Next")
    if len(next_button) > 0:
        next_button.links.find_by_partial_text("Next").click()
    
def log_data(data, page_num):
    log_number_parsed = len(data)
    with open('log.txt', 'a') as file:
        file.write(f'Parsed {log_number_parsed} quotes on page number {page_num + 1}.\n')

def make_csv(data):
    csv_path = 'resources/scraped_data.csv'
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    return csv_path