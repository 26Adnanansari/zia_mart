import os
from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use the service-specific database URL for PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL_ORDER")

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session