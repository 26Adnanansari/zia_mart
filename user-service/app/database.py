import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# Load environment variables from the container's environment
load_dotenv()

# Use the appropriate database URL based on the environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")  # Defaults to "production"
DATABASE_URL = None

if ENVIRONMENT == "test":
    DATABASE_URL = os.getenv("TEST_DATABASE_URL_USER")
else:
    DATABASE_URL = os.getenv("DATABASE_URL_USER")

# Fallback if DATABASE_URL is still None
if not DATABASE_URL:
    raise ValueError("No database URL provided. Please set DATABASE_URL_USER or TEST_DATABASE_URL_USER in your .env file.")

# Print the selected database URL for debugging
print(f"Environment: {ENVIRONMENT}")
print(f"Using Database URL: {DATABASE_URL}")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Example usage
if __name__ == "__main__":
    create_db_and_tables()