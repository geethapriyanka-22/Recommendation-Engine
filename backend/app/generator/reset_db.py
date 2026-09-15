"""
NovaMart — Database Reset & Authentic Data Seeder

Safely wipes the entire database and seeds it with genuine, recognizable
brand products, high-resolution imagery, realistic reviews, and vector embeddings.
"""

import asyncio
import logging

from app.core.database import async_session_factory
from app.generator.synthetic_data import SyntheticDataGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("novamart.reset")


async def main():
    logger.info("⚡ Starting NovaMart database wipe & authentic reseed...")
    async with async_session_factory() as session:
        generator = SyntheticDataGenerator(session)
        await generator.wipe_database()
        stats = await generator.generate_all()
        await session.commit()
        logger.info(f"🎉 Reseed successful! Final stats: {stats}")


if __name__ == "__main__":
    asyncio.run(main())
