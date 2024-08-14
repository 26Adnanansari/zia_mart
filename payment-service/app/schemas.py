from pydantic import BaseModel
from datetime import datetime

class PaymentCreate(BaseModel):
    amount: float
    currency: str
    payment_method_id: int

class PaymentRead(BaseModel):
    id: int
    amount: float
    currency: str
    status: str
    payment_method_id: int
    created_at: datetime

class TransactionCreate(BaseModel):
    payment_id: int
    transaction_id: str
    gateway: str
    amount: float
    currency: str

class TransactionRead(BaseModel):
    id: int
    payment_id: int
    transaction_id: str
    gateway: str
    amount: float
    currency: str
    status: str
    created_at: datetime