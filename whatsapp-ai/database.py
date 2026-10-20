import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

#create db connection_engine
engine = create_engine(DATABASE_URL)
#Create a session factoryy to handle db transaction
SessionLocal = sessionmaker(autocommit = False, autoflush=False,bind=engine)
#Baseclass for our python models
Base = declarative_base()
#dependency to safely open and close db connections
# Double check the spelling here: 'get_db'
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
