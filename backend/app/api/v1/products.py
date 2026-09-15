"""
NovaMart — Product Routes

CRUD, listing with filters, and slug-based access.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import allow_admin, allow_seller_admin, get_current_user
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService

router = APIRouter()


@router.get("", response_model=ProductListResponse, include_in_schema=False)
@router.get("/", response_model=ProductListResponse)
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category_id: UUID | None = None,
    category: str | None = None,
    brand: str | None = None,
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    min_rating: float | None = Query(None, ge=0, le=5),
    in_stock: bool | None = None,
    sort_by: str = Query("created_at", pattern="^(created_at|price_asc|price_desc|rating|title)$"),
    q: str | None = None,
    db: AsyncSession = Depends(get_async_session),
):
    """List products with filtering, search, and pagination."""
    service = ProductService(db)
    products, total = await service.list_products(
        skip=skip,
        limit=limit,
        category_id=category_id,
        category=category,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        in_stock=in_stock,
        sort_by=sort_by,
        q=q,
    )
    return ProductListResponse(
        items=[ProductResponse.model_validate(p) for p in products],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """Get a product by ID."""
    service = ProductService(db)
    product = await service.get_by_id(product_id)
    return ProductResponse.model_validate(product)


@router.get("/slug/{slug}", response_model=ProductResponse)
async def get_product_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_async_session),
):
    """Get a product by its URL slug."""
    service = ProductService(db)
    product = await service.get_by_slug(slug)
    return ProductResponse.model_validate(product)


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate,
    current_user: User = Depends(allow_seller_admin),
    db: AsyncSession = Depends(get_async_session),
):
    """Create a new product (seller/admin only)."""
    service = ProductService(db)
    product = await service.create(data)
    return ProductResponse.model_validate(product)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    data: ProductUpdate,
    current_user: User = Depends(allow_seller_admin),
    db: AsyncSession = Depends(get_async_session),
):
    """Update a product (seller for own products / admin for any)."""
    service = ProductService(db)
    product = await service.update(product_id, data)
    return ProductResponse.model_validate(product)


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: UUID,
    current_user: User = Depends(allow_admin),
    db: AsyncSession = Depends(get_async_session),
):
    """Delete a product (admin only)."""
    service = ProductService(db)
    await service.delete(product_id)
