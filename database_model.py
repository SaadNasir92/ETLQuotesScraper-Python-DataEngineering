# Imports
from sqlalchemy import create_engine, text, Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import text


def engineer_model(database_name: str, password: str, def_connection: str):
    """
    Create the database schema and return an SQLAlchemy engine connected to the new database.

    Args:
        database_name (str): The name of the new database to create.
        password (str): The password for the database user.
        def_connection (str): The default database connection string.

    Returns:
        Engine: An SQLAlchemy engine connected to the newly created database.
    """
    database_name = create_db(database_name, def_connection)
    new_db_url = f"postgresql+psycopg2://postgres:{password}@localhost:5432/{database_name}"

    engine = create_engine(new_db_url)
    Base = declarative_base()

    class Author(Base):
        """
        Represents the author table in the database.
        
        Attributes:
        auth_id (int): The primary key for the author table.
        author (str): The name of the author.
        quotes (relationship): A relationship to the Quote class.
        """
        __tablename__ = 'author'
        auth_id = Column(Integer, primary_key=True, autoincrement=True)
        author = Column(String(50), nullable=False, unique=True)
        quotes = relationship('Quote', back_populates='author')

    class Quote(Base):
        """
        Represents the quote table in the database.
    
        Attributes:
        quote_id (int): The primary key for the quote table.
        quote (str): The text of the quote.
        auth_id (int): The foreign key to the author table.
        author (relationship): A relationship to the Author class.
        tags (relationship): A many-to-many relationship to the Tag class through quote_tag.
        """
        __tablename__ = 'quote'
        quote_id = Column(Integer, primary_key=True, autoincrement=True)
        quote = Column(Text, nullable=False)
        auth_id = Column(Integer, ForeignKey('author.auth_id'), nullable=False)
        author = relationship('Author', back_populates='quotes')
        tags = relationship('Tag', secondary='quote_tag', back_populates='quotes')

    class Tag(Base):
        """
        Represents the tag table in the database.
    
        Attributes:
        tag_id (int): The primary key for the tag table.
        tag (str): The text of the tag.
        quotes (relationship): A many-to-many relationship to the Quote class through quote_tag.
        """
        __tablename__ = 'tag'
        tag_id = Column(Integer, primary_key=True, autoincrement=True)
        tag = Column(String(50), nullable=False, unique=True)
        quotes = relationship('Quote', secondary='quote_tag', back_populates='tags')

    Quote_tag = Table('quote_tag', Base.metadata,
        Column('quote_id', Integer, ForeignKey('quote.quote_id'), primary_key=True),
        Column('tag_id', Integer, ForeignKey('tag.tag_id'), primary_key=True)
    )

    Base.metadata.create_all(engine)
    
    return engine

def create_db(db_name: str, db_url: str) -> str:
    """
    Create a new PostgreSQL database with the given name.

    Args:
        db_name (str): The name of the database to create.
        db_url (str): The connection URL to the default database.

    Returns:
        str: The cleaned name of the newly created database to use within the engineer_model function to connect to the newly created database from this function.
    """
    db_name = clean_name(db_name)

    engine = create_engine(db_url, isolation_level='AUTOCOMMIT')
    
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE {db_name}"))
        print(f"Database {db_name} created.")

    return db_name

def clean_name(name: str) -> str:
    """
    Clean and format a string to be used as a database name.

    Args:
        name (str): The name to clean.

    Returns:
        str: The cleaned and formatted name.
    """
    name = name.lower()
    name = name.replace(' ', '_')
    
    return name
