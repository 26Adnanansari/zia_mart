from typing import Optional
from sqlmodel import Session, select
from app.models import Order

def create_order(session: Session, order: Order) -> Order:
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def get_order(session: Session, order_id: int) -> Optional[Order]:
    return session.get(Order, order_id)

def get_orders(session: Session, skip: int = 0, limit: int = 10):
    return session.exec(select(Order).offset(skip).limit(limit)).all()

def update_order(session: Session, order_id: int, order_data: dict) -> Optional[Order]:
    order = session.get(Order, order_id)
    if order:
        for key, value in order_data.items():
            setattr(order, key, value)
        session.add(order)
        session.commit()
        session.refresh(order)
    return order

def delete_order(session: Session, order_id: int) -> bool:
    order = session.get(Order, order_id)
    if order:
        session.delete(order)
        session.commit()
        return True
    return False