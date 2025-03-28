from datetime import datetime
from sqlalchemy import Boolean, CheckConstraint, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
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
    # accept_token: Mapped[List['Token']] = relationship(back_populates='user')


# class Token(Base):
#     __tablename__ = 'accept_tokens'

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     jti: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id",
# ondelete='CASCADE'))
#     #user: Mapped['User'] = relationship(back_populates='accept_token')
