from datetime import datetime
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., description="Название товара")
    price: float = Field(..., description="Цена товара")


class ProductCreate(ProductBase):
    id: int = Field(..., description="ID товара")
    description: str = Field(..., description="Описание")


class ProductResponse(ProductBase):
    id: int = Field(..., description="ID товара")
    description: str = Field(..., description="Описание")
    created_at: datetime = Field(..., description="Дата создания")