"""
NovaMart — Category Schemas
"""

from uuid import UUID

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = None
    icon: str | None = None
    parent_id: UUID | None = None
    sort_order: int = 0


class CategoryChildResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: str | None = None
    icon: str | None = None
    parent_id: UUID | None = None
    sort_order: int = 0

    model_config = {"from_attributes": True}


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: str | None = None
    icon: str | None = None
    parent_id: UUID | None = None
    sort_order: int = 0
    children: list[CategoryChildResponse] = []

    model_config = {"from_attributes": True}
