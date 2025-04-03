from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from online_store.app.api.auth import get_current_user
from online_store.app.db.base import get_db
from online_store.app.db.models import Product, User
from online_store.app.schema.product_schema import ProductCreate, ProductResponse

product_router = APIRouter(prefix='/products', tags=['products'])


@product_router.get('', response_model=List[ProductResponse])
def get_all_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Product).all()


@product_router.post('/create', response_model=ProductResponse)
def create_product(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    input_product: ProductCreate = None
):
    product_check = db.query(Product).filter(
        input_product.name == Product.name).first()

    if product_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name already registered"
            )

    new_product = Product(
        name=input_product.name,
        price=input_product.price,
        description=input_product.description,
        created_at=datetime.now()
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
