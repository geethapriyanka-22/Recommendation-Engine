"""
NovaMart — Category Routes
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_async_session
from app.core.dependencies import allow_admin
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryResponse
from app.schemas.product import ProductListResponse, ProductResponse
from app.services.product_service import ProductService

from slugify import slugify

router = APIRouter()


@router.get("", response_model=list[CategoryResponse], include_in_schema=False)
@router.get("/", response_model=list[CategoryResponse])
async def list_categories(
    db: AsyncSession = Depends(get_async_session),
):
    """Get the full category tree (top-level with nested children)."""
    result = await db.execute(
        select(Category)
        .options(selectinload(Category.children))
        .where(Category.parent_id == None)
        .order_by(Category.sort_order)
    )
    categories = result.scalars().unique().all()
    return [CategoryResponse.model_validate(c) for c in categories]


@router.get("/{category_id}/products", response_model=ProductListResponse)
async def list_category_products(
    category_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at", pattern="^(created_at|price_asc|price_desc|rating|title)$"),
    db: AsyncSession = Depends(get_async_session),
):
    """List products in a specific category."""
    service = ProductService(db)
    products, total = await service.list_products(
        skip=skip, limit=limit, category_id=category_id, sort_by=sort_by
    )
    return ProductListResponse(
        items=[ProductResponse.model_validate(p) for p in products],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    current_user: User = Depends(allow_admin),
    db: AsyncSession = Depends(get_async_session),
):
    """Create a new category (admin only)."""
    category = Category(
        name=data.name,
        slug=slugify(data.name),
        description=data.description,
        icon=data.icon,
        parent_id=data.parent_id,
        sort_order=data.sort_order,
    )
    db.add(category)
    await db.flush()
    return CategoryResponse.model_validate(category)
