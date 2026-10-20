from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL='postgresql://postgres: @localhost/fastapi'
# this is the connection string to connect to the database. It contains the username, password, ip address/hostname and database name.

engine = create_engine(SQLALCHEMY_DATABASE_URL)#used to create a connection to the database. It takes the connection string as an argument and returns an engine object that can be used to interact with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# this is a factory function that creates a new session object. It takes the engine object as an argument and returns a session object that can be used to interact with the database.
Base = declarative_base()# this is a base class for our database models. It is used to create the tables in the database and to define the structure of the data that we want to store in the database.

# Dependency to open and close your database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()