# Then query the tables from python
# Then graph the counts of tags.

#imports 
import os
from etl import perform_etl

# website & number of pages to scrape
website = "http://quotes.toscrape.com/"
pages_to_scrape = 10

# grab path to csv to check whether etl needs to be performed.
csv_path = os.path.join('resources', 'scraped_data.csv')

def main(path_to_csv):
    # run ETL if scrape hasn't happened
    if not os.path.exists(path_to_csv):
        print('CSV file not found, performing ETL')
        perform_etl(website, pages_to_scrape)
    else:
        print('Data has already been scraped transformed and loaded in the database.')

if __name__ == "__main__":
    main(csv_path)
   
