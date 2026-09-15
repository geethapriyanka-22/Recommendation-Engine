"""
NovaMart — Cart Routes
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartResponse, CartItemResponse
from app.services.cart_service import CartService

router = APIRouter()


def _build_cart_response(cart) -> CartResponse:
    """Build a CartResponse with computed totals from a Cart ORM object."""
    items = []
    total = 0.0

    for item in cart.items:
        product = item.product
        line_total = float(product.price) * item.quantity
        total += line_total

        image_url = None
        if product.images:
            image_url = product.images[0].url

        items.append(CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_title=product.title,
            product_price=float(product.price),
            product_image=image_url,
            quantity=item.quantity,
            line_total=line_total,
        ))

    return CartResponse(
        id=cart.id,
        items=items,
        item_count=len(items),
        total=round(total, 2),
    )


@router.get("", response_model=CartResponse, include_in_schema=False)
@router.get("/", response_model=CartResponse)
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Get the current user's cart."""
    service = CartService(db)
    cart = await service.get_or_create_cart(current_user.id)
    return _build_cart_response(cart)


@router.post("/items", response_model=CartResponse)
async def add_to_cart(
    data: CartItemAdd,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Add a product to the cart."""
    service = CartService(db)
    cart = await service.add_item(current_user.id, data.product_id, data.quantity)
    return _build_cart_response(cart)


@router.put("/items/{item_id}", response_model=CartResponse)
async def update_cart_item(
    item_id: UUID,
    data: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Update a cart item's quantity."""
    service = CartService(db)
    cart = await service.update_item(current_user.id, item_id, data.quantity)
    return _build_cart_response(cart)


@router.delete("/items/{item_id}", response_model=CartResponse)
async def remove_cart_item(
    item_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Remove an item from the cart."""
    service = CartService(db)
    cart = await service.remove_item(current_user.id, item_id)
    return _build_cart_response(cart)


@router.delete("/", status_code=204)
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Clear the entire cart."""
    service = CartService(db)
    await service.clear_cart(current_user.id)
