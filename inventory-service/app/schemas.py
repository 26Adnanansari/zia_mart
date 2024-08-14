from pydantic import BaseModel

class InventoryItemCreate(BaseModel):
    product_id: int
    quantity: int

class InventoryItemRead(InventoryItemCreate):
    id: int

    class Config:
        orm_mode = True