"""
NovaMart — Order Routes
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.order import (
    CheckoutRequest,
    OrderListResponse,
    OrderResponse,
)
from app.services.order_service import OrderService

router = APIRouter()


@router.post("/checkout", response_model=OrderResponse, status_code=201)
async def checkout(
    data: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Create an order from the current cart (atomic transaction)."""
    service = OrderService(db)
    order = await service.checkout(
        user_id=current_user.id,
        shipping_address_id=data.shipping_address_id,
        notes=data.notes,
    )
    return OrderResponse.model_validate(order)


@router.get("", response_model=OrderListResponse, include_in_schema=False)
@router.get("/", response_model=OrderListResponse)
async def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """List the current user's orders."""
    service = OrderService(db)
    orders, total = await service.list_user_orders(current_user.id, skip, limit)
    return OrderListResponse(
        items=[OrderResponse.model_validate(o) for o in orders],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Get a specific order (own orders only)."""
    service = OrderService(db)
    order = await service.get_by_id(order_id, current_user.id)
    return OrderResponse.model_validate(order)


@router.patch("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Cancel a pending order (restores stock)."""
    service = OrderService(db)
    order = await service.cancel_order(order_id, current_user.id)
    return OrderResponse.model_validate(order)
