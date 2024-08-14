from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    total_price: float

class OrderRead(OrderCreate):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True