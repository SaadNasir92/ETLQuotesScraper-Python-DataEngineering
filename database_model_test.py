from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import declarative_base, Session
from private_info import postgres_pw
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, MetaData
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import text



def create_db(db_name, db_url):
    # Connect to the default database (typically 'postgres') to check for the existence of the target database
    engine = create_engine(db_url)
    connection = engine.connect()
    db_name = clean_name(db_name)
    connection.execute(text(f"CREATE DATABASE {db_name}"))
    print(f"Database {db_name} created.")
    connection.close()
    return db_name
    
def clean_name(name):
    name = name.lower()
    name = name.replace(' ', '_')
    return name



def engineer_model(database_name: str, password, def_connection):
    
    database_name = create_db(database_name, def_connection)
    new_db_url = f"postgresql+psycopg2://username:{password}@localhost:5432/{database_name}"

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
        quote = Column(String(255), nullable=False)
        auth_id = Column(Integer, ForeignKey('author.auth_id'), nullable=False)
        author = relationship('Author', back_populates='quotes')
        tags = relationship('Tag', secondary='quote_tag', back_populates='quotes')

    class Tag(Base):
        __tablename__ = 'tag'
        tag_id = Column(Integer, primary_key=True, autoincrement=True)
        tag = Column(String(25), nullable=False, unique=True)
        quotes = relationship('Quote', secondary='quote_tag', back_populates='tags')

    Quote_tag = Table('quote_tag', Base.metadata,
        Column('quote_id', Integer, ForeignKey('quote.quote_id'), primary_key=True),
        Column('tag_id', Integer, ForeignKey('tag.tag_id'), primary_key=True)
    )

    Base.metadata.create_all(engine)
    
    return engine
