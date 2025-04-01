from datetime import datetime
from typing import List
from sqlalchemy import (
    Boolean, CheckConstraint, ForeignKey, Integer, String, DateTime
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


