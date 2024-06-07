# Weekend challenge: go through first 10 pages, extract the text, author, tags. 
# Then create a database, either sqlite or postgres, 
# Then insert your results from scraping into the tables in your data base
# Then query the tables from python
# Then graph the counts of tags.
# Please apply functional programming paradigm meaning, convert all your codes to reusable functions.
from scrape import perform_scrape

website = "http://quotes.toscrape.com/"
pages_to_scrape = 10

all_data = perform_scrape(website, pages_to_scrape)
print(len(all_data))


