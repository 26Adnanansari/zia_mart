from typing import Optional
from sqlmodel import Session, select
from app.models import InventoryItem

def create_inventory_item(session: Session, item: InventoryItem) -> InventoryItem:
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

def get_inventory_item(session: Session, item_id: int) -> Optional[InventoryItem]:
    return session.get(InventoryItem, item_id)

def get_inventory_items(session: Session, skip: int = 0, limit: int = 10):
    return session.exec(select(InventoryItem).offset(skip).limit(limit)).all()

def update_inventory_item(session: Session, item_id: int, item_data: dict) -> Optional[InventoryItem]:
    item = session.get(InventoryItem, item_id)
    if item:
        for key, value in item_data.items():
            setattr(item, key, value)
        session.add(item)
        session.commit()
        session.refresh(item)
    return item

def delete_inventory_item(session: Session, item_id: int) -> bool:
    item = session.get(InventoryItem, item_id)
    if item:
        session.delete(item)
        session.commit()
        return True
    return False