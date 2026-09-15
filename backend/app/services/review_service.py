"""
NovaMart — Review Service

Review CRUD with automatic product rating recalculation.
"""

import uuid
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewUpdate


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_for_product(
        self, product_id: uuid.UUID
    ) -> tuple[list[dict], int, float]:
        """List all reviews for a product with user names."""
        result = await self.db.execute(
            select(Review, User.full_name)
            .join(User, Review.user_id == User.id)
            .where(Review.product_id == product_id)
            .order_by(Review.created_at.desc())
        )
        rows = result.all()

        reviews = []
        for review, user_name in rows:
            reviews.append({
                "id": review.id,
                "product_id": review.product_id,
                "user_id": review.user_id,
                "user_name": user_name,
                "rating": review.rating,
                "title": review.title,
                "body": review.body,
                "is_verified_purchase": review.is_verified_purchase,
                "created_at": review.created_at,
            })

        total = len(reviews)
        avg_rating = sum(r["rating"] for r in reviews) / total if total > 0 else 0.0

        return reviews, total, avg_rating

    async def create(
        self, product_id: uuid.UUID, user_id: uuid.UUID, data: ReviewCreate
    ) -> Review:
        """Create a review (one per user per product)."""
        # Check product exists
        product_result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )
        if not product_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        # Check for existing review
        existing = await self.db.execute(
            select(Review).where(
                Review.product_id == product_id,
                Review.user_id == user_id,
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already reviewed this product",
            )

        # Check if this is a verified purchase
        order_result = await self.db.execute(
            select(OrderItem.id)
            .join(Order, OrderItem.order_id == Order.id)
            .where(
                Order.user_id == user_id,
                OrderItem.product_id == product_id,
            )
            .limit(1)
        )
        is_verified = order_result.scalar_one_or_none() is not None

        review = Review(
            product_id=product_id,
            user_id=user_id,
            rating=data.rating,
            title=data.title,
            body=data.body,
            is_verified_purchase=is_verified,
        )
        self.db.add(review)
        await self.db.flush()

        # Recalculate product rating
        await self._recalculate_product_rating(product_id)

        return review

    async def update(
        self, review_id: uuid.UUID, user_id: uuid.UUID, data: ReviewUpdate
    ) -> Review:
        """Update own review."""
        result = await self.db.execute(
            select(Review).where(Review.id == review_id, Review.user_id == user_id)
        )
        review = result.scalar_one_or_none()

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(review, field, value)

        await self.db.flush()
        await self._recalculate_product_rating(review.product_id)
        return review

    async def delete(
        self, review_id: uuid.UUID, user_id: uuid.UUID, is_admin: bool = False
    ) -> None:
        """Delete a review (own or admin)."""
        query = select(Review).where(Review.id == review_id)
        if not is_admin:
            query = query.where(Review.user_id == user_id)

        result = await self.db.execute(query)
        review = result.scalar_one_or_none()

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

        product_id = review.product_id
        await self.db.delete(review)
        await self.db.flush()
        await self._recalculate_product_rating(product_id)

    async def _recalculate_product_rating(self, product_id: uuid.UUID) -> None:
        """Recalculate avg_rating and review_count for a product."""
        result = await self.db.execute(
            select(
                func.count(Review.id),
                func.coalesce(func.avg(Review.rating), 0),
            ).where(Review.product_id == product_id)
        )
        count, avg = result.one()

        product_result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )
        product = product_result.scalar_one()
        product.review_count = count
        product.avg_rating = round(float(avg), 2)
        await self.db.flush()
