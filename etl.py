# Import modules
from scrape import perform_scrape
from database_model import engineer_model
from data_load import dump_data

# Import global variables
from schema_config import MODEL_SCHEMA
from private_info import POSTGRES_PW, DEFAULT_DB_URL

def perform_etl(url: str, num_pages: int):
    """
    Perform the ETL (Extract, Transform, Load) process for scraping and loading quotes data.

    Args:
        url (str): The URL of the website to scrape.
        num_pages (int): The number of pages to scrape.
    """
    # get csv file path for scraped data
    scraped_file_path = perform_scrape(url, num_pages)

    # create database in postgres and make tables and constraints
    engine = engineer_model('popular_quotes', POSTGRES_PW, DEFAULT_DB_URL)

    # clean/transform data from csv to follow database constraints, then load data.
    dump_data(scraped_file_path, MODEL_SCHEMA, engine)