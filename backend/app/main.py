"""
NovaMart — FastAPI Application Entry Point

Application factory with lifespan management, middleware, and auto-seeding.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text

from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.database import async_session_factory, engine
from app.models.base import Base
from app.models.user import User
from app.models.category import Category
from app.models.product import Product, ProductImage, ProductEmbedding
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem, Address
from app.models.review import Review

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("novamart")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle: run migrations, enable extensions, seed data."""
    logger.info(f"🚀 Starting {settings.APP_NAME} ({settings.ENVIRONMENT})")

    # Create all tables (dev convenience — in prod, use Alembic exclusively)
    async with engine.begin() as conn:
        # Enable required PostgreSQL extensions
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "vector"'))
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "pg_trgm"'))

        await conn.run_sync(Base.metadata.create_all)
        logger.info("  ✅ Database tables ready")

    # Auto-seed if enabled and database is empty
    if settings.SEED_ON_STARTUP:
        async with async_session_factory() as session:
            result = await session.execute(select(User).limit(1))
            if not result.scalar_one_or_none():
                logger.info("  🌱 Empty database detected — running seed...")
                from app.generator.synthetic_data import SyntheticDataGenerator

                generator = SyntheticDataGenerator(session)
                stats = await generator.generate_all()
                await session.commit()
                logger.info(f"  🌱 Seed complete: {stats}")
            else:
                logger.info("  ℹ️  Database already seeded, skipping")

    logger.info(f"  🟢 {settings.APP_NAME} is ready!")
    logger.info(f"  📄 API docs: http://localhost:8000/docs")

    yield

    # Shutdown
    await engine.dispose()
    logger.info(f"  🔴 {settings.APP_NAME} shut down")


# ─── Create Application ─────────────────────────────────
# ─── Create Application ─────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered E-Commerce Platform with Semantic Search & Product Recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    redirect_slashes=False,
)

# ─── CORS Middleware ─────────────────────────────────────
_cors_origins = list(set(
    settings.cors_origins_list + [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
))

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Mount Routes ────────────────────────────────────────
app.include_router(api_v1_router)


@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "app": settings.APP_NAME, "version": "1.0.0"}
