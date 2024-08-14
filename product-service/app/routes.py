from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.database import get_session
from app.models import Product
from app.schemas import ProductCreate, ProductRead
from app.crud import create_product, get_product, get_products, update_product, delete_product

router = APIRouter()

@router.post("/products/", response_model=ProductRead)
def create_new_product(product: ProductCreate, session: Session = Depends(get_session)):
    return create_product(session, Product.from_orm(product))

@router.get("/products/{product_id}", response_model=ProductRead)
def read_product(product_id: int, session: Session = Depends(get_session)):
    product = get_product(session, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/products/", response_model=list[ProductRead])
def read_products(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return get_products(session, skip, limit)

@router.put("/products/{product_id}", response_model=ProductRead)
def update_existing_product(product_id: int, product: ProductCreate, session: Session = Depends(get_session)):
    updated_product = update_product(session, product_id, product.dict(exclude_unset=True))
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/products/{product_id}")
def delete_existing_product(product_id: int, session: Session = Depends(get_session)):
    success = delete_product(session, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"ok": True}