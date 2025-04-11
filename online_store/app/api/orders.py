from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload,selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from online_store.app.db.models import User, Product, CartItem, Order, OrderItem
from online_store.app.db.base import get_db
from online_store.app.api.auth import get_current_user
from online_store.app.api.cart import get_user_cart


order_router = APIRouter(prefix="/orders", tags=["Orders"])


async def create_order_from_cart(db: AsyncSession, user: User):

    # cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).join(Product).all()
    cart_items = await db.execute(
        select(CartItem).filter(CartItem.user_id == user.id).join(Product).options(selectinload(CartItem.product))
    )
    cart_items = cart_items.scalars().all()
    print(cart_items)
    if not cart_items:
        raise ValueError("Cart is empty")

    # Создаем заказ
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    print(total_amount)
    order = Order(user_id=user.id, total_amount=total_amount)
    print(order)
    db.add(order)
    await db.flush()

    # Создаем элементы заказа
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        db.add(order_item)
        db.delete(cart_item)  # Удаляем товар из корзины
    await db.commit()
    await db.refresh(order)
    return order


async def get_user_orders(db: AsyncSession, user: User):
    # orders = db.query(Order).where(Order.user_id == user.id).join(OrderItem).join(Product).all()
    orders = await db.execute(
        select(Order).where(Order.user_id == user.id).join(OrderItem).join(Product).options(selectinload(Order.order_items).selectinload(OrderItem.product))
    )
    orders = orders.scalars().all()

    order_details = []
    for order in orders:
        # order_items = db.query(OrderItem).where(OrderItem.order_id == order.id).join(Product).all()
        order_items = await db.execute(
                select(OrderItem).where(OrderItem.order_id == order.id).join(Product).options(selectinload(OrderItem.product))
            )
        order_items = order_items.scalars().all()
        
        items = []
        for item in order_items:
            items.append({
                "product_id": item.product.id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
                "total": item.price * item.quantity
            })

        order_details.append({
            "order_id": order.id,
            "status": order.status.value,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "items": items
        })

    return order_details



@order_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order_endpoint(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        order = await create_order_from_cart(db, current_user)
        return {
            "message": "Order created successfully",
            "oreder": order
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    

@order_router.get("/", status_code=status.HTTP_200_OK)
async def get_user_orders_endpoint(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        orders = await get_user_orders(db, current_user)
        return orders
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))