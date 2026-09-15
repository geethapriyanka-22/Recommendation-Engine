"""
NovaMart — Admin Routes

Dashboard stats, user management, order management, data seeding, and reindexing.
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_async_session
from app.core.dependencies import allow_admin
from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.models.user import User, UserRole
from app.schemas.order import OrderListResponse, OrderResponse, OrderStatusUpdate
from app.schemas.user import UserResponse, UserRoleUpdate
from app.services.order_service import OrderService
from app.services.vector_service import VectorService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/dashboard")
async def dashboard_stats(
    current_user: User = Depends(allow_admin),
    db: AsyncSession = Depends(get_async_session),
):
    """Get high-level dashboard statistics."""
    # Total counts
    users_count = (await db.execute(select(func.count(User.id)))).scalar() or 0
    products_count = (await db.execute(select(func.count(Product.id)))).scalar() or 0
    orders_count = (await db.execute(select(func.count(Order.id)))).scalar() or 0

    # Revenue
    revenue_result = await db.execute(
        select(func.coalesce(func.sum(Order.total), 0)).where(
            Order.status.notin_([OrderStatus.CANCELLED, OrderStatus.REFUNDED])
        )
    )
    total_revenue = float(revenue_result.scalar())

    # Low stock products
    low_stock = (
        await db.execute(
            select(func.count(Product.id)).where(
                Product.stock_quantity < 5,
                Product.is_published == True,
            )
        )
    ).scalar() or 0

    # Orders by status
    status_result = await db.execute(
        select(Order.status, func.count(Order.id)).group_by(Order.status)
    )
    orders_by_status = {row[0].value: row[1] for row in status_result.all()}

    return {
        "total_users": users_count,
        "total_products": products_count,
        "total_orders": orders_count,
        "total_revenue": round(total_revenue, 2),
        "low_stock_products": low_stock,
        "orders_by_status": orders_by_status,
    }


@router.get("/users", response_model=list[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(allow_admin),
    db: AsyncSession = Depends(get_async_session),
):
    """List all users."""
    result = await db.execute(
        select(User).order_by(User.created_at.desc()).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    return [UserResponse.model_validate(u) for u in users]


@router.patch("/users/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: UUID,
    data: UserRoleUpdate,
    current_user: User = Depends(allow_admin),
    db: AsyncSession = Depends(get_async_session),
):
    """Change a user's role."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        from fastapi import HTTPException
        raise HTTPException(404, "User not found")

    user.role = UserRole(data.role)
    await db.flush()
    return UserResponse.model_validate(user)


@router.patch("/orders/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: UUID,
    data: OrderStatusUpdate,
    current_user: User = Depends(allow_admin),
    db: AsyncSession = Depends(get_async_session),
):
    """Update an order's status (follows state machine)."""
    service = OrderService(db)
    order = await service.update_status(order_id, data.status)
    return OrderResponse.model_validate(order)


@router.get("/orders", response_model=OrderListResponse)
async def list_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: str | None = None,
    current_user: User = Depends(allow_admin),
    db: AsyncSession = Depends(get_async_session),
):
    """List all orders (admin view)."""
    service = OrderService(db)
    orders, total = await service.list_all_orders(skip, limit, status)
    return OrderListResponse(
        items=[OrderResponse.model_validate(o) for o in orders],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post("/seed")
async def seed_data(
    current_user: User = Depends(allow_admin),
    db: AsyncSession = Depends(get_async_session),
):
    """Run the synthetic data generator."""
    from app.generator.synthetic_data import SyntheticDataGenerator

    generator = SyntheticDataGenerator(db)
    stats = await generator.generate_all()
    return {"message": "Seed data generated successfully", "stats": stats}


@router.post("/reindex-embeddings")
async def reindex_embeddings(
    current_user: User = Depends(allow_admin),
    db: AsyncSession = Depends(get_async_session),
):
    """Re-generate embeddings for all products."""
    result = await db.execute(
        select(Product).options(selectinload(Product.category))
    )
    products = list(result.scalars().all())

    service = VectorService(db)
    count = await service.bulk_generate_embeddings(products)
    return {"message": f"Re-indexed {count} product embeddings"}
