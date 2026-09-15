"""
NovaMart — AI / Search Schemas
"""

from uuid import UUID

from pydantic import BaseModel, Field


class SemanticSearchRequest(BaseModel):
    q: str = Field(..., min_length=2, max_length=500)
    limit: int = Field(10, ge=1, le=50)
    min_price: float | None = None
    max_price: float | None = None
    category_id: UUID | None = None


class SearchResultItem(BaseModel):
    id: UUID
    title: str
    slug: str
    short_description: str
    price: float
    compare_at_price: float | None
    brand: str | None
    avg_rating: float
    review_count: int
    image_url: str | None
    relevance_score: float

    model_config = {"from_attributes": True}


class SemanticSearchResponse(BaseModel):
    query: str
    results: list[SearchResultItem]
    total: int


class RecommendationResponse(BaseModel):
    source_product_id: UUID
    recommendations: list[SearchResultItem]


class PersonalizedRecommendationResponse(BaseModel):
    items: list[SearchResultItem]
    reason: str
    is_personalized: bool

