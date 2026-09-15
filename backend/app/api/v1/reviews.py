"""
NovaMart — Review Routes
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.review import (
    ReviewCreate,
    ReviewListResponse,
    ReviewResponse,
    ReviewUpdate,
)
from app.services.review_service import ReviewService

router = APIRouter()


@router.get("/products/{product_id}/reviews", response_model=ReviewListResponse)
async def list_reviews(
    product_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """List all reviews for a product."""
    service = ReviewService(db)
    reviews, total, avg_rating = await service.list_for_product(product_id)
    return ReviewListResponse(
        items=[ReviewResponse(**r) for r in reviews],
        total=total,
        avg_rating=round(avg_rating, 2),
    )


@router.post(
    "/products/{product_id}/reviews",
    response_model=ReviewResponse,
    status_code=201,
)
async def create_review(
    product_id: UUID,
    data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Create a review for a product (one per user)."""
    service = ReviewService(db)
    review = await service.create(product_id, current_user.id, data)
    return ReviewResponse.model_validate(review)


@router.put("/products/{product_id}/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(
    product_id: UUID,
    review_id: UUID,
    data: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Update own review."""
    service = ReviewService(db)
    review = await service.update(review_id, current_user.id, data)
    return ReviewResponse.model_validate(review)


@router.delete("/products/{product_id}/reviews/{review_id}", status_code=204)
async def delete_review(
    product_id: UUID,
    review_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Delete own review (or any review if admin)."""
    service = ReviewService(db)
    is_admin = current_user.role.value == "admin"
    await service.delete(review_id, current_user.id, is_admin=is_admin)
