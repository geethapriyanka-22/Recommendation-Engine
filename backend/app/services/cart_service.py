"""
NovaMart — Cart Service

Cart management with stock validation.
"""

import uuid
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart import Cart, CartItem
from app.models.product import Product


class CartService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_cart(self, user_id: uuid.UUID) -> Cart:
        """Get the user's cart, creating one if it doesn't exist."""
        result = await self.db.execute(
            select(Cart)
            .options(
                selectinload(Cart.items).selectinload(CartItem.product).selectinload(Product.images),
            )
            .where(Cart.user_id == user_id)
        )
        cart = result.scalar_one_or_none()

        if not cart:
            cart = Cart(user_id=user_id)
            self.db.add(cart)
            await self.db.flush()
            # Re-fetch with relationships
            result = await self.db.execute(
                select(Cart)
                .options(
                    selectinload(Cart.items).selectinload(CartItem.product).selectinload(Product.images),
                )
                .where(Cart.id == cart.id)
            )
            cart = result.scalar_one()

        return cart

    async def add_item(
        self, user_id: uuid.UUID, product_id: uuid.UUID, quantity: int
    ) -> Cart:
        """Add an item to the cart or increment quantity if already present."""
        # Validate product exists and is in stock
        product_result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )
        product = product_result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        if not product.is_published:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is not available",
            )
        if product.stock_quantity < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {product.stock_quantity} units available",
            )

        cart = await self.get_or_create_cart(user_id)

        # Check if product already in cart
        existing_item = None
        for item in cart.items:
            if item.product_id == product_id:
                existing_item = item
                break

        if existing_item:
            new_qty = existing_item.quantity + quantity
            if new_qty > product.stock_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot add more. Only {product.stock_quantity} units available",
                )
            existing_item.quantity = new_qty
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
            )
            self.db.add(cart_item)

        await self.db.flush()
        self.db.expire(cart)
        return await self.get_or_create_cart(user_id)

    async def update_item(
        self, user_id: uuid.UUID, item_id: uuid.UUID, quantity: int
    ) -> Cart:
        """Update the quantity of a cart item."""
        cart = await self.get_or_create_cart(user_id)

        item = None
        for cart_item in cart.items:
            if cart_item.id == item_id:
                item = cart_item
                break

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found",
            )

        # Validate stock
        product_result = await self.db.execute(
            select(Product).where(Product.id == item.product_id)
        )
        product = product_result.scalar_one()

        if quantity > product.stock_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {product.stock_quantity} units available",
            )

        item.quantity = quantity
        await self.db.flush()
        self.db.expire(cart)
        return await self.get_or_create_cart(user_id)

    async def remove_item(self, user_id: uuid.UUID, item_id: uuid.UUID) -> Cart:
        """Remove an item from the cart."""
        cart = await self.get_or_create_cart(user_id)

        item = None
        for cart_item in cart.items:
            if cart_item.id == item_id:
                item = cart_item
                break

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found",
            )

        await self.db.delete(item)
        await self.db.flush()
        self.db.expire(cart)
        return await self.get_or_create_cart(user_id)

    async def clear_cart(self, user_id: uuid.UUID) -> None:
        """Remove all items from the cart."""
        cart = await self.get_or_create_cart(user_id)
        for item in cart.items:
            await self.db.delete(item)
        await self.db.flush()
        self.db.expire(cart)
