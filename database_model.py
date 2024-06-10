from sqlalchemy import create_engine, text, Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import text


def engineer_model(database_name: str, password, def_connection):
    
    database_name = create_db(database_name, def_connection)
    new_db_url = f"postgresql+psycopg2://postgres:{password}@localhost:5432/{database_name}"

    engine = create_engine(new_db_url)
    Base = declarative_base()

    class Author(Base):
        __tablename__ = 'author'
        auth_id = Column(Integer, primary_key=True, autoincrement=True)
        author = Column(String(50), nullable=False, unique=True)
        quotes = relationship('Quote', back_populates='author')

    class Quote(Base):
        __tablename__ = 'quote'
        quote_id = Column(Integer, primary_key=True, autoincrement=True)
        quote = Column(Text, nullable=False)
        auth_id = Column(Integer, ForeignKey('author.auth_id'), nullable=False)
        author = relationship('Author', back_populates='quotes')
        tags = relationship('Tag', secondary='quote_tag', back_populates='quotes')

    class Tag(Base):
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

def create_db(db_name, db_url):
    # Connect to the default database (typically 'postgres') to check for the existence of the target database
    db_name = clean_name(db_name)

    engine = create_engine(db_url, isolation_level='AUTOCOMMIT')
    
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE {db_name}"))
        print(f"Database {db_name} created.")

    return db_name

def clean_name(name):
    name = name.lower()
    name = name.replace(' ', '_')
    return name
