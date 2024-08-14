from fastapi import FastAPI
from app.routes import router as user_router
from app.database import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()  # Ensure the database and tables are created on startup

app.include_router(user_router)