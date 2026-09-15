import asyncio
from app.core.database import async_session_factory
from app.services.product_service import ProductService

async def main():
    async with async_session_factory() as s:
        svc = ProductService(s)
        for term in ["mobile", "phone", "sneakers", "cream", "laptop"]:
            prods, count = await svc.list_products(q=term, limit=5)
            print(f"\nQuery: '{term}' -> Found {count} items:")
            for p in prods:
                print(f"  - {p.title} (${p.price})")

if __name__ == "__main__":
    asyncio.run(main())
