from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    currency: str
    status: str
    payment_method_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

class PaymentMethod(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    method_name: str
    description: Optional[str] = None

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    payment_id: int = Field(foreign_key="payment.id")
    transaction_id: str
    gateway: str
    amount: float
    currency: str
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)