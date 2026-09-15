"""
NovaMart — Product Schemas
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProductImageResponse(BaseModel):
    id: UUID
    url: str
    alt_text: str | None
    sort_order: int

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=300)
    description: str = Field(..., min_length=20)
    short_description: str = Field(..., min_length=10, max_length=500)
    price: float = Field(..., gt=0)
    compare_at_price: float | None = Field(None, gt=0)
    stock_quantity: int = Field(0, ge=0)
    category_id: UUID
    brand: str | None = Field(None, max_length=100)
    attributes: dict = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    is_published: bool = False
    is_featured: bool = False


class ProductUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=300)
    description: str | None = Field(None, min_length=20)
    short_description: str | None = Field(None, min_length=10, max_length=500)
    price: float | None = Field(None, gt=0)
    compare_at_price: float | None = Field(None, gt=0)
    stock_quantity: int | None = Field(None, ge=0)
    category_id: UUID | None = None
    brand: str | None = Field(None, max_length=100)
    attributes: dict | None = None
    tags: list[str] | None = None
    is_published: bool | None = None
    is_featured: bool | None = None


class ProductResponse(BaseModel):
    id: UUID
    sku: str
    title: str
    slug: str
    description: str
    short_description: str
    price: float
    compare_at_price: float | None
    stock_quantity: int
    category_id: UUID
    brand: str | None
    attributes: dict
    tags: list[str]
    avg_rating: float
    review_count: int
    is_published: bool
    is_featured: bool
    images: list[ProductImageResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    skip: int
    limit: int
