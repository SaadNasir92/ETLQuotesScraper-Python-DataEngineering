# Quotes Scraper and Database Loader

## Objective

The objective of this project is to scrape quotes, authors, and tags from a specified website, transform the scraped data to adhere to normalization principles, and load the cleaned data into a PostgreSQL database using Object-Relational Mapping (ORM) with SQLAlchemy.

## Approach

This project follows a structured Extract, Transform, Load (ETL) process to ensure that the scraped data is accurately and efficiently stored in a normalized relational database. The approach includes the following steps:

1. **Scraping Data**: Quotes, authors, and tags are scraped from a specified website using Splinter and BeautifulSoup.
2. **Transforming Data**: The scraped data is cleaned and transformed to meet database constraints and normalization principles.
3. **Loading Data**: The transformed data is loaded into a PostgreSQL database using SQLAlchemy's ORM methodology.

### Step-by-Step Approach

1. **Scraping Data**:
    - The `perform_scrape` function initiates the scraping process.
    - A browser instance is created using Splinter's `Browser` class.
    - The `scrape_web` function navigates through the specified number of pages, extracting quotes, authors, and tags using BeautifulSoup.
    - The scraped data is logged and saved to a CSV file.

2. **Transforming Data**:
    - The `dump_data` function reads the scraped data from the CSV file.
    - The `prepare_dataframes` function processes the data, ensuring it adheres to the schema defined in `MODEL_SCHEMA`.
    - Data transformations include removing duplicates, creating primary keys, and merging dataframes based on foreign key relationships.

3. **Loading Data**:
    - The `engineer_model` function creates the necessary tables and constraints in a PostgreSQL database using SQLAlchemy's ORM.
    - The `load_table` function inserts the transformed data into the respective tables in the database.

## ORM Methodology on PostgreSQL

### Database Models

The project defines the following ORM models using SQLAlchemy:

1. **Author Model**:
    ```python
    class Author(Base):
        __tablename__ = 'author'
        auth_id = Column(Integer, primary_key=True, autoincrement=True)
        author = Column(String(50), nullable=False, unique=True)
        quotes = relationship('Quote', back_populates='author')
    ```

2. **Quote Model**:
    ```python
    class Quote(Base):
        __tablename__ = 'quote'
        quote_id = Column(Integer, primary_key=True, autoincrement=True)
        quote = Column(Text, nullable=False)
        auth_id = Column(Integer, ForeignKey('author.auth_id'), nullable=False)
        author = relationship('Author', back_populates='quotes')
        tags = relationship('Tag', secondary='quote_tag', back_populates='quotes')
    ```

3. **Tag Model**:
    ```python
    class Tag(Base):
        __tablename__ = 'tag'
        tag_id = Column(Integer, primary_key=True, autoincrement=True)
        tag = Column(String(50), nullable=False, unique=True)
        quotes = relationship('Quote', secondary='quote_tag', back_populates='tags')
    ```

4. **Quote-Tag Association Table**:
    ```python
    quote_tag = Table('quote_tag', Base.metadata,
        Column('quote_id', Integer, ForeignKey('quote.quote_id'), primary_key=True),
        Column('tag_id', Integer, ForeignKey('tag.tag_id'), primary_key=True)
    )
    ```

## SUMMARY
This project effectively demonstrates a robust ETL pipeline that adheres to database normalization principles. By leveraging web scraping, data transformation, and ORM methodologies, it ensures data integrity and efficient storage in a relational database.


