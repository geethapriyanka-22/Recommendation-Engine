"""
NovaMart — Supabase Database Initializer & Seeder

Creates all tables, enables extensions, seeds users, categories, products,
reviews, orders, and builds vector embeddings.
"""

import asyncio
import logging
import os
import sys

# Ensure backend root is on python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import select, text
from app.core.database import async_session_factory, engine
from app.models.base import Base
import app.models  # Register all models: User, Product, Category, Order, Review, etc.
from app.models.user import User
from app.generator.synthetic_data import SyntheticDataGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed_supabase")


async def main():
    logger.info("Connecting to database...")
    
    # 1. Create tables
    async with engine.begin() as conn:
        logger.info("Ensuring PostgreSQL extensions exist...")
        try:
            await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
            await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "vector";'))
            await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "pg_trgm";'))
        except Exception as e:
            logger.warning(f"Note on extensions (they might already be enabled via UI): {e}")

        logger.info("Creating all database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ All tables created successfully!")

    # 2. Seed database
    async with async_session_factory() as session:
        result = await session.execute(select(User).limit(1))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            logger.info("Database already contains data. Running catalog sync...")
        else:
            logger.info("Seeding complete catalog, users, categories, and embeddings...")
            generator = SyntheticDataGenerator(session)
            stats = await generator.generate_all()
            await session.commit()
            logger.info(f"✅ Seeding finished successfully: {stats}")

    await engine.dispose()
    logger.info("🎉 Database setup complete!")


if __name__ == "__main__":
    asyncio.run(main())
