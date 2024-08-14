from fastapi import FastAPI
from app.database import init_db  # Make sure this matches exactly with the function name in database.py
from app.routes import router as product_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(product_router)