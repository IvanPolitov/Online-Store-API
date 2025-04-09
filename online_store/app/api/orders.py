from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from online_store.app.db.models import User, Product, CartItem, Order, OrderItem
from online_store.app.db.base import get_db
from online_store.app.api.auth import get_current_user
from online_store.app.api.cart import get_user_cart


order_router = APIRouter(prefix="/orders", tags=["Orders"])


def create_order_from_cart(db: Session, user: User):

    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).join(Product).all()

    if not cart_items:
        raise ValueError("Cart is empty")

    # Создаем заказ
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    order = Order(user_id=user.id, total_amount=total_amount)
    db.add(order)
    db.flush()

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
    db.commit()
    return order


async def get_user_orders(db: Session, user: User):


    orders = db.query(Order).where(Order.user_id == user.id).join(OrderItem).join(Product).all()

    order_details = []
    for order in orders:
        order_items = db.query(OrderItem).where(OrderItem.order_id == order.id).join(Product).all()

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
def create_order_endpoint(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    try:
        order = create_order_from_cart(session, current_user)
        return {
            "message": "Order created successfully",
            "order_id": order.id,
            "total_amount": order.total_amount,
            "status": order.status.value
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    

@order_router.get("/", status_code=status.HTTP_200_OK)
async def get_user_orders_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        orders = await get_user_orders(db, current_user)
        return orders
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))