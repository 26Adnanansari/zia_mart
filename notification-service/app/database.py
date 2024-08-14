import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use the appropriate database URL based on the environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")  # Defaults to "production"
if ENVIRONMENT == "test":
    DATABASE_URL = os.getenv("TEST_DATABASE_URL_NOTIFICATION")
else:
    DATABASE_URL = os.getenv("DATABASE_URL_NOTIFICATION")

if not DATABASE_URL:
    raise ValueError("No database URL provided. Please set DATABASE_URL_NOTIFICATION or TEST_DATABASE_URL_NOTIFICATION in your .env file.")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)