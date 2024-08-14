from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

class ProductRead(ProductCreate):
    id: int

    class Config:
        orm_mode = True