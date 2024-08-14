from sqlmodel import Session
from .models import Notification

def send_notification(user_id: int, message: str, session: Session):
    notification = Notification(user_id=user_id, message=message)
    session.add(notification)
    session.commit()
    # Here you can add logic to actually send the notification (email, SMS, etc.)
    print(f"Notification sent to user {user_id}: {message}")