from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from online_store.app.api.auth import get_current_user
from online_store.app.db.base import get_db
from online_store.app.db.models import Product, User
from online_store.app.schema.product_schema import ProductCreate, ProductResponse

product_router = APIRouter(prefix='/products', tags=['products'])


@product_router.get('', response_model=List[ProductResponse])
async def get_all_products(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # return db.query(Product).all()
    users = await db.execute(select(Product))
    users = users.scalars().all()

    return users



@product_router.post('/create', response_model=ProductResponse)
async def create_product(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    input_product: ProductCreate = None
):
    # product_check = db.query(Product).filter(
    #     input_product.name == Product.name).first()
    product_check = await db.execute(
        select(Product).where(input_product.name == Product.name)
    )
    product_check = product_check.scalar()

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
    await db.commit()
    await db.refresh(new_product)

    return new_product
