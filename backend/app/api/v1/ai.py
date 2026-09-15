"""
NovaMart — AI / Semantic Search Routes

Hybrid vector + FTS search and embedding-based recommendations.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import get_current_user_optional
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem
from app.models.user import User
from app.schemas.ai import (
    PersonalizedRecommendationResponse,
    RecommendationResponse,
    SearchResultItem,
    SemanticSearchResponse,
)
from app.services.vector_service import VectorService

router = APIRouter()


def _product_to_search_result(product, score: float) -> SearchResultItem:
    """Convert a Product ORM object + score to a SearchResultItem."""
    image_url = None
    if product.images:
        image_url = product.images[0].url

    return SearchResultItem(
        id=product.id,
        title=product.title,
        slug=product.slug,
        short_description=product.short_description,
        price=float(product.price),
        compare_at_price=float(product.compare_at_price) if product.compare_at_price else None,
        brand=product.brand,
        avg_rating=float(product.avg_rating),
        review_count=product.review_count,
        image_url=image_url,
        relevance_score=round(score, 4),
    )


@router.get("/semantic-search", response_model=SemanticSearchResponse)
async def semantic_search(
    q: str = Query(..., min_length=2, max_length=500),
    limit: int = Query(10, ge=1, le=50),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    category_id: UUID | None = None,
    category: str | None = None,
    db: AsyncSession = Depends(get_async_session),
):
    """
    AI-powered semantic search using hybrid scoring:
    vector similarity (0.60) + full-text ranking (0.25) + popularity (0.15).
    """
    service = VectorService(db)
    results = await service.semantic_search(
        query=q,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
        category_id=category_id,
        category=category,
    )
    return SemanticSearchResponse(
        query=q,
        results=[_product_to_search_result(p, s) for p, s in results],
        total=len(results),
    )


@router.get("/recommendations/{product_id}", response_model=RecommendationResponse)
async def get_recommendations(
    product_id: UUID,
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_async_session),
):
    """Get semantically similar product recommendations with strict category alignment."""
    service = VectorService(db)
    results = await service.get_recommendations(product_id, limit)
    return RecommendationResponse(
        source_product_id=product_id,
        recommendations=[_product_to_search_result(p, s) for p, s in results],
    )


@router.get("/personalized-recommendations", response_model=PersonalizedRecommendationResponse)
async def get_personalized_recommendations(
    product_ids: str | None = Query(None, description="Comma-separated product IDs from client activity (visited, cart, purchased)"),
    search_queries: str | None = Query(None, description="Comma-separated recent search terms from client activity"),
    limit: int = Query(4, ge=1, le=20),
    current_user: User | None = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Generate dynamic homepage recommendations based on user interactions
    (visited, added to cart, or purchased products, plus recent search queries).
    """
    interacted_uuids: list[UUID] = []
    parsed_queries: list[str] = []

    # 1. Parse client-passed interaction IDs and search queries
    if product_ids:
        for raw_id in product_ids.split(","):
            raw_clean = raw_id.strip()
            if raw_clean:
                try:
                    interacted_uuids.append(UUID(raw_clean))
                except ValueError:
                    pass

    if search_queries:
        for sq in search_queries.split(","):
            sq_clean = sq.strip()
            if sq_clean and sq_clean not in parsed_queries:
                parsed_queries.append(sq_clean)

    # 2. If logged in, supplement with database order and cart history
    if current_user:
        try:
            from sqlalchemy import select
            # Check user's recent orders
            order_res = await db.execute(
                select(OrderItem.product_id)
                .join(Order, OrderItem.order_id == Order.id)
                .where(Order.user_id == current_user.id)
                .order_by(Order.created_at.desc())
                .limit(10)
            )
            for pid in order_res.scalars().all():
                if pid and pid not in interacted_uuids:
                    interacted_uuids.append(pid)

            # Check user's current cart
            cart_res = await db.execute(
                select(CartItem.product_id)
                .join(Cart, CartItem.cart_id == Cart.id)
                .where(Cart.user_id == current_user.id)
            )
            for pid in cart_res.scalars().all():
                if pid and pid not in interacted_uuids:
                    interacted_uuids.append(pid)
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Could not load user DB interactions: {e}")

    service = VectorService(db)
    result = await service.get_personalized_recommendations(
        interacted_ids=interacted_uuids,
        search_queries=parsed_queries,
        limit=limit,
    )

    return PersonalizedRecommendationResponse(
        items=[_product_to_search_result(p, s) for p, s in result["recommendations"]],
        reason=result["reason"],
        is_personalized=result["is_personalized"],
    )

