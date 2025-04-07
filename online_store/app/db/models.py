from datetime import datetime
from typing import List
from sqlalchemy import (
    Boolean, CheckConstraint, Float, ForeignKey, Integer, String, DateTime
    )
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, CheckConstraint("age <= 18"))
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())
    cart_items = relationship("CartItem", back_populates="user")

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String, default='No description')
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())
    cart_items = relationship("CartItem", back_populates="product")

class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped['User'] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    product_id: Mapped['Product'] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
