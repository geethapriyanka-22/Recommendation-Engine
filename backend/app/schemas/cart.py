"""
NovaMart — Cart Schemas
"""

from uuid import UUID

from pydantic import BaseModel, Field


class CartItemAdd(BaseModel):
    product_id: UUID
    quantity: int = Field(1, gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    product_title: str | None = None
    product_price: float | None = None
    product_image: str | None = None
    quantity: int
    line_total: float | None = None

    model_config = {"from_attributes": True}


class CartResponse(BaseModel):
    id: UUID
    items: list[CartItemResponse] = []
    item_count: int = 0
    total: float = 0.0
