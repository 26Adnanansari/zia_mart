from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.database import get_session
from app.models import Order
from app.schemas import OrderCreate, OrderRead
from app.crud import create_order, get_order, get_orders, update_order, delete_order

router = APIRouter()

@router.post("/orders/", response_model=OrderRead)
def create_new_order(order: OrderCreate, session: Session = Depends(get_session)):
    # Use model_validate instead of from_orm
    order_obj = Order.model_validate(order)
    return create_order(session, order_obj)

@router.get("/orders/{order_id}", response_model=OrderRead)
def read_order(order_id: int, session: Session = Depends(get_session)):
    order = get_order(session, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders/", response_model=list[OrderRead])
def read_orders(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return get_orders(session, skip, limit)

@router.put("/orders/{order_id}", response_model=OrderRead)
def update_existing_order(order_id: int, order: OrderCreate, session: Session = Depends(get_session)):
    updated_order = update_order(session, order_id, order.dict(exclude_unset=True))
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/orders/{order_id}")
def delete_existing_order(order_id: int, session: Session = Depends(get_session)):
    success = delete_order(session, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"ok": True}