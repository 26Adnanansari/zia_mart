from fastapi import FastAPI, Depends
from .database import init_db, get_session
from .notification import send_notification
from sqlmodel import Session

app = FastAPI()

# Initialize the database
@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/notify/")
async def notify_user(user_id: int, message: str, session: Session = Depends(get_session)):
    send_notification(user_id, message, session)
    return {"status": "Notification sent"}