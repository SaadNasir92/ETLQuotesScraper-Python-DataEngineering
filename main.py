# Weekend challenge: go through first 10 pages, extract the text, author, tags. 
# Then create a database, either sqlite or postgres, 
# Then insert your results from scraping into the tables in your data base
# Then query the tables from python
# Then graph the counts of tags.
# Please apply functional programming paradigm meaning, convert all your codes to reusable functions.
from scrape import perform_scrape
from database_model_test import engineer_model
from data_load import dump_data
from schema_config import config
from private_info import postgres_pw, db_url_default

model_schema = config
website = "http://quotes.toscrape.com/"
pages_to_scrape = 10

scraped_file_path = perform_scrape(website, pages_to_scrape)

engine = engineer_model('popular_quotes')

data_to_load = dump_data(scraped_file_path, model_schema, engine)

print(data_to_load)









