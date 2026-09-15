"""
NovaMart — Order Schemas
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CheckoutRequest(BaseModel):
    shipping_address_id: UUID | None = None
    notes: str | None = None


class OrderItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    product_title: str
    product_sku: str
    quantity: int
    unit_price: float
    total_price: float

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: UUID
    order_number: str
    status: str
    subtotal: float
    tax_amount: float
    total: float
    notes: str | None
    items: list[OrderItemResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    items: list[OrderResponse]
    total: int
    skip: int
    limit: int


class OrderStatusUpdate(BaseModel):
    status: str = Field(
        ...,
        pattern="^(pending|confirmed|processing|shipped|delivered|cancelled|refunded)$",
    )
