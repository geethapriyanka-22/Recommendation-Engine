"""
NovaMart — Order Service

Atomic checkout, order lifecycle, and status management.
"""

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem, OrderStatus, ORDER_STATUS_TRANSITIONS
from app.models.product import Product


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def checkout(
        self,
        user_id: uuid.UUID,
        shipping_address_id: uuid.UUID | None = None,
        notes: str | None = None,
    ) -> Order:
        """
        Atomic checkout: validate stock → create order → decrement stock → clear cart.

        All operations run within a single transaction.
        """
        # 1. Load the user's cart with items and products
        result = await self.db.execute(
            select(Cart)
            .options(
                selectinload(Cart.items).selectinload(CartItem.product),
            )
            .where(Cart.user_id == user_id)
        )
        cart = result.scalar_one_or_none()

        if not cart or not cart.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty",
            )

        # 2. Validate stock and calculate totals
        subtotal = Decimal("0.00")
        order_items_data = []

        for cart_item in cart.items:
            product = cart_item.product

            if not product.is_published:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product '{product.title}' is no longer available",
                )

            if product.stock_quantity < cart_item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for '{product.title}'. Available: {product.stock_quantity}",
                )

            line_total = Decimal(str(product.price)) * cart_item.quantity
            subtotal += line_total

            order_items_data.append({
                "product_id": product.id,
                "product_title": product.title,
                "product_sku": product.sku,
                "quantity": cart_item.quantity,
                "unit_price": product.price,
                "total_price": float(line_total),
            })

        # 3. Calculate tax (8% flat rate for demo)
        tax_amount = float(subtotal * Decimal("0.08"))
        total = float(subtotal) + tax_amount

        # 4. Generate order number
        order_number = await self._generate_order_number()

        # 5. Create order
        order = Order(
            order_number=order_number,
            user_id=user_id,
            status=OrderStatus.PENDING,
            shipping_address_id=shipping_address_id,
            subtotal=float(subtotal),
            tax_amount=tax_amount,
            total=total,
            notes=notes,
        )
        self.db.add(order)
        await self.db.flush()

        # 6. Create order items
        for item_data in order_items_data:
            order_item = OrderItem(order_id=order.id, **item_data)
            self.db.add(order_item)

        # 7. Decrement stock
        for cart_item in cart.items:
            product = cart_item.product
            product.stock_quantity -= cart_item.quantity

        # 8. Clear cart
        for cart_item in cart.items:
            await self.db.delete(cart_item)

        await self.db.flush()

        # Re-fetch with relationships
        return await self.get_by_id(order.id, user_id)

    async def get_by_id(
        self, order_id: uuid.UUID, user_id: uuid.UUID | None = None
    ) -> Order:
        """Get an order by ID, optionally scoped to a user."""
        query = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        if user_id:
            query = query.where(Order.user_id == user_id)

        result = await self.db.execute(query)
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        return order

    async def list_user_orders(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[Order], int]:
        """List orders for a specific user."""
        query = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        orders = list(result.scalars().unique().all())

        count_result = await self.db.execute(
            select(func.count(Order.id)).where(Order.user_id == user_id)
        )
        total = count_result.scalar() or 0

        return orders, total

    async def list_all_orders(
        self, skip: int = 0, limit: int = 20, status_filter: str | None = None
    ) -> tuple[list[Order], int]:
        """List all orders (admin). Optionally filter by status."""
        query = select(Order).options(selectinload(Order.items))
        count_query = select(func.count(Order.id))

        if status_filter:
            query = query.where(Order.status == OrderStatus(status_filter))
            count_query = count_query.where(Order.status == OrderStatus(status_filter))

        query = query.order_by(Order.created_at.desc()).offset(skip).limit(limit)

        result = await self.db.execute(query)
        orders = list(result.scalars().unique().all())

        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        return orders, total

    async def cancel_order(self, order_id: uuid.UUID, user_id: uuid.UUID) -> Order:
        """Cancel a pending order and restore stock."""
        order = await self.get_by_id(order_id, user_id)

        if order.status not in (OrderStatus.PENDING, OrderStatus.CONFIRMED):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot cancel order with status '{order.status.value}'",
            )

        # Restore stock
        for item in order.items:
            product_result = await self.db.execute(
                select(Product).where(Product.id == item.product_id)
            )
            product = product_result.scalar_one()
            product.stock_quantity += item.quantity

        order.status = OrderStatus.CANCELLED
        await self.db.flush()
        return order

    async def update_status(
        self, order_id: uuid.UUID, new_status: str
    ) -> Order:
        """Admin: update order status following the state machine."""
        order = await self.get_by_id(order_id)
        new_status_enum = OrderStatus(new_status)

        allowed = ORDER_STATUS_TRANSITIONS.get(order.status, [])
        if new_status_enum not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition from '{order.status.value}' to '{new_status}'. Allowed: {[s.value for s in allowed]}",
            )

        order.status = new_status_enum
        await self.db.flush()
        return order

    async def _generate_order_number(self) -> str:
        """Generate a unique human-readable order number."""
        date_part = datetime.now(timezone.utc).strftime("%Y%m%d")
        count_result = await self.db.execute(select(func.count(Order.id)))
        count = (count_result.scalar() or 0) + 1
        return f"ORD-{date_part}-{count:04d}"
