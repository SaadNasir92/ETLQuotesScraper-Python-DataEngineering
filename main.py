# Then query the tables from python
# Then graph the counts of tags.
# Please apply functional programming paradigm meaning, convert all your codes to reusable functions.

# Import modules
from scrape import perform_scrape
from database_model import engineer_model
from data_load import dump_data

# Import global variables
from schema_config import MODEL_SCHEMA
from private_info import POSTGRES_PW, DEFAULT_DB_URL

# website & number of pages to scrape
website = "http://quotes.toscrape.com/"
pages_to_scrape = 10

# get csv file path for scraped data
scraped_file_path = perform_scrape(website, pages_to_scrape)

# create database in postgres and make tables and constraints
engine = engineer_model('popular_quotes', POSTGRES_PW, DEFAULT_DB_URL)

# clean/transform data from csv to follow database constraints, then load data.
data_to_load = dump_data(scraped_file_path, MODEL_SCHEMA, engine)










