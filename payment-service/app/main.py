from fastapi import FastAPI
from app.database import create_db_and_tables  # Make sure this matches exactly with the function name in database.py
from app.routes import router as payment_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(payment_router)