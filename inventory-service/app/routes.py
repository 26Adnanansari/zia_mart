from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.database import get_session
from app.models import InventoryItem
from app.schemas import InventoryItemCreate, InventoryItemRead
from app.crud import create_inventory_item, get_inventory_item, get_inventory_items, update_inventory_item, delete_inventory_item

router = APIRouter()

@router.post("/inventory/", response_model=InventoryItemRead)
def create_new_inventory_item(item: InventoryItemCreate, session: Session = Depends(get_session)):
    inventory_item = create_inventory_item(session, InventoryItem.from_orm(item))
    return inventory_item

@router.get("/inventory/{item_id}", response_model=InventoryItemRead)
def read_inventory_item(item_id: int, session: Session = Depends(get_session)):
    item = get_inventory_item(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/inventory/", response_model=list[InventoryItemRead])
def read_inventory_items(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return get_inventory_items(session, skip, limit)

@router.put("/inventory/{item_id}", response_model=InventoryItemRead)
def update_existing_inventory_item(item_id: int, item: InventoryItemCreate, session: Session = Depends(get_session)):
    updated_item = update_inventory_item(session, item_id, item.dict(exclude_unset=True))
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/inventory/{item_id}")
def delete_existing_inventory_item(item_id: int, session: Session = Depends(get_session)):
    success = delete_inventory_item(session, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}