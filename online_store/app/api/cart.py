from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from online_store.app.api.auth import get_current_user
from online_store.app.db.base import get_db
from online_store.app.db.models import Product, User, CartItem


cart_router = APIRouter(prefix='/cart', tags=['cart'])


async def add_product_to_cart(db: AsyncSession, user: User, product_id: int, quantity: int = 1):
    user_id = user.id

    # product = db.query(Product).filter(Product.id == product_id).first()
    product = await db.execute(
        select(Product).filter(Product.id == product_id)
    )
    product = product.scalar()

    if not product:
        raise ValueError("Product not found")
    
    # cart_item = db.query(CartItem).filter((CartItem.user_id == user_id) & (CartItem.product_id == product.id)).first()
    cart_item = await db.execute(
        select(CartItem).filter((CartItem.user_id == user_id) & (CartItem.product_id == product.id))
        )
    cart_item = cart_item.scalar()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
            )
        db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)


async def get_user_cart(db: AsyncSession, user: User):

    user_id = user.id

    # cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    cart_items = await db.execute(
        select(CartItem).filter(CartItem.user_id == user_id).options(joinedload(CartItem.product))
    )
    cart_items = cart_items.scalars().all()
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No cart"
            )
    cart_contents = []
    for item in cart_items:
        cart_contents.append({
            "product_id": item.product.id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price": item.product.price,
            "total": item.product.price * item.quantity
        })

    return cart_contents


@cart_router.post("/add/{product_id}", status_code=status.HTTP_201_CREATED)
async def add_product_to_cart_endpoint(
    product_id: int,
    quantity: int = 1,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        await add_product_to_cart(db, current_user, product_id, quantity)
        return {"message": "Product added to cart"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    

@cart_router.get("/", status_code=status.HTTP_200_OK)
async def get_user_cart_endpoint(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        cart_contents = await get_user_cart(db, current_user)
        return cart_contents
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    