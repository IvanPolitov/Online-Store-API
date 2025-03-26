from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50,
                          description="Имя пользователя")
    email: EmailStr = Field(..., description="Электронная почта")
    age: int = Field(..., ge=18, description="Возраст")
    is_active: Optional[bool] = Field(
        True, description="Активен ли пользователь")


class UserCreate(UserBase):
    password_hash: str = Field(..., description="Пароль")


class UserResponse(UserBase):
    id: int = Field(..., description="ID пользователя")
    created_at: datetime = Field(..., description="Дата создания")

    class Config:
        orm_mode = True
