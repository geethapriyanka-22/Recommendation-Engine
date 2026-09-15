"""
NovaMart — API v1 Router Aggregator

Collects all v1 route modules into a single router.
"""

from fastapi import APIRouter

from app.api.v1 import admin, ai, auth, cart, categories, orders, products, reviews

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(products.router, prefix="/products", tags=["Products"])
api_v1_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_v1_router.include_router(cart.router, prefix="/cart", tags=["Cart"])
api_v1_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_v1_router.include_router(reviews.router, tags=["Reviews"])
api_v1_router.include_router(ai.router, prefix="/ai", tags=["AI & Search"])
api_v1_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
