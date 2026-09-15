"""
Script to reindex all product embeddings using FastEmbed.
"""

import asyncio
import os
import sys

# Support UTF-8 stdout on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure backend directory is in python path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import async_session_factory
from app.models.product import Product
from app.services.vector_service import VectorService


async def main():
    print("🚀 Starting FastEmbed embedding generation for all products...")
    async with async_session_factory() as session:
        result = await session.execute(
            select(Product).options(selectinload(Product.category))
        )
        products = list(result.scalars().all())
        print(f"📦 Found {len(products)} products to embed.")

        if not products:
            print("❌ No products found in database.")
            return

        service = VectorService(session)
        count = await service.bulk_generate_embeddings(products)
        await session.commit()
        print(f"✅ Successfully generated and saved {count} genuine FastEmbed embeddings!")


if __name__ == "__main__":
    asyncio.run(main())
