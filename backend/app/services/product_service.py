"""
NovaMart — Product Service

Product CRUD, filtering, pagination, and search operations.
"""

import uuid
from decimal import Decimal

from fastapi import HTTPException, status
from slugify import slugify
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.product import Product, ProductImage
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate


SYNONYMS: dict[str, list[str]] = {
    "mobile": ["mobile", "phone", "smartphone", "cellular", "iphone", "android", "galaxy", "pixel", "smartphones & tablets"],
    "mobiles": ["mobile", "phone", "smartphone", "cellular", "iphone", "android", "galaxy", "pixel"],
    "phone": ["phone", "smartphone", "mobile", "cellular", "iphone", "android", "smartphones & tablets"],
    "phones": ["phone", "smartphone", "mobile", "cellular", "iphone", "android"],
    "smartphone": ["smartphone", "phone", "mobile", "iphone", "android", "samsung", "pixel"],
    "smartphones": ["smartphone", "phone", "mobile", "iphone", "android", "samsung", "pixel"],
    "laptop": ["laptop", "macbook", "notebook", "computer", "pc", "xps", "thinkpad", "laptops & computers"],
    "laptops": ["laptop", "macbook", "notebook", "computer", "pc", "xps", "thinkpad"],
    "computer": ["computer", "pc", "laptop", "macbook", "desktop", "laptops & computers"],
    "computers": ["computer", "pc", "laptop", "macbook", "desktop"],
    "pc": ["pc", "computer", "laptop", "desktop"],
    "shoe": ["shoe", "shoes", "sneaker", "sneakers", "footwear", "loafers", "runners", "sneakers & footwear"],
    "shoes": ["shoe", "shoes", "sneaker", "sneakers", "footwear", "loafers", "runners"],
    "sneaker": ["sneaker", "sneakers", "shoes", "footwear", "runners"],
    "sneakers": ["sneaker", "sneakers", "shoes", "footwear", "runners"],
    "cloth": ["clothing", "apparel", "jacket", "coat", "jeans", "shirt", "dress", "fashion"],
    "clothes": ["clothing", "apparel", "jacket", "coat", "jeans", "shirt", "dress", "fashion"],
    "clothing": ["clothing", "apparel", "jacket", "coat", "jeans", "shirt", "dress", "fashion"],
    "apparel": ["clothing", "apparel", "jacket", "coat", "jeans", "shirt", "fashion"],
    "jacket": ["jacket", "coat", "outerwear", "parka", "trench", "blazer", "jackets & outerwear"],
    "jackets": ["jacket", "coat", "outerwear", "parka", "trench", "blazer"],
    "coat": ["coat", "trench", "jacket", "outerwear", "gabardine", "overcoat", "jackets & outerwear"],
    "coats": ["coat", "trench", "jacket", "outerwear", "gabardine", "overcoat"],
    "bag": ["bag", "handbag", "purse", "backpack", "tote", "crossbody", "luggage", "bags & luggage"],
    "bags": ["bag", "handbag", "purse", "backpack", "tote", "crossbody", "luggage"],
    "watch": ["watch", "smartwatch", "timepiece", "chronograph", "garmin", "apple watch", "gps & sports watches"],
    "watches": ["watch", "smartwatch", "timepiece", "chronograph", "garmin", "apple watch"],
    "headphone": ["headphone", "headphones", "earbuds", "earphones", "audio", "sony", "audio & headphones"],
    "headphones": ["headphone", "headphones", "earbuds", "earphones", "audio", "sony"],
    "earphone": ["earphone", "earphones", "earbuds", "headphones", "audio"],
    "earphones": ["earphone", "earphones", "earbuds", "headphones", "audio"],
    "audio": ["audio", "headphone", "headphones", "speaker", "sound", "sonos", "audio & headphones"],
    "speaker": ["speaker", "speakers", "audio", "sound", "sonos"],
    "speakers": ["speaker", "speakers", "audio", "sound", "sonos"],
    "perfume": ["perfume", "fragrance", "cologne", "parfum", "scent", "baccarat", "fragrances & perfumes"],
    "perfumes": ["perfume", "fragrance", "cologne", "parfum", "scent"],
    "fragrance": ["fragrance", "perfume", "cologne", "parfum", "scent", "fragrances & perfumes"],
    "fragrances": ["fragrance", "perfume", "cologne", "parfum", "scent"],
    "cream": ["cream", "moisturizer", "skincare", "lotion", "serum", "bader", "skincare treatments"],
    "skincare": ["skincare", "cream", "moisturizer", "serum", "beauty", "skincare treatments"],
    "cookware": ["cookware", "dutch oven", "cast iron", "pot", "pan", "le creuset", "cookware & dining"],
    "coffee": ["coffee", "espresso", "kettle", "fellow", "barista", "breville", "moccamaster"],
}


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _resolve_category_ids(
        self,
        category_id: uuid.UUID | None = None,
        category: str | None = None,
    ) -> list[uuid.UUID] | None:
        """Resolve a category (by ID, slug, or name) and include all of its subcategory IDs."""
        target_id: uuid.UUID | None = None

        if category_id:
            target_id = category_id
        elif category:
            cat_str = category.strip()
            try:
                target_id = uuid.UUID(cat_str)
            except ValueError:
                norm_slug = cat_str.lower().replace("_", "-")
                cat_result = await self.db.execute(
                    select(Category.id).where(
                        or_(
                            Category.slug == norm_slug,
                            Category.slug == cat_str.lower(),
                            Category.name.ilike(cat_str),
                        )
                    ).order_by(Category.parent_id.nulls_first())
                )
                target_id = cat_result.scalars().first()
                if not target_id:
                    sub_result = await self.db.execute(
                        select(Category.id).where(Category.slug.ilike(f"%{norm_slug}%"))
                        .order_by(Category.parent_id.nulls_first())
                    )
                    target_id = sub_result.scalars().first()

        if not target_id:
            if category:
                return []
            return None

        child_res = await self.db.execute(
            select(Category.id).where(Category.parent_id == target_id)
        )
        child_ids = list(child_res.scalars().all())
        return [target_id] + child_ids

    async def list_products(
        self,
        skip: int = 0,
        limit: int = 20,
        category_id: uuid.UUID | None = None,
        category: str | None = None,
        brand: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_rating: float | None = None,
        in_stock: bool | None = None,
        sort_by: str = "created_at",
        q: str | None = None,
        published_only: bool = True,
    ) -> tuple[list[Product], int]:
        """List products with filtering, pagination, synonym expansion, and semantic fallback."""
        query = select(Product).options(selectinload(Product.images))
        count_query = select(func.count(Product.id.distinct()))

        # Base filter: only published products for non-admin
        filters = []
        if published_only:
            filters.append(Product.is_published == True)

        # Resolve category (slug or ID) including subcategories
        cat_ids = await self._resolve_category_ids(category_id=category_id, category=category)
        if cat_ids is not None:
            if len(cat_ids) == 0:
                return [], 0
            filters.append(Product.category_id.in_(cat_ids))

        if brand:
            filters.append(Product.brand.ilike(f"%{brand}%"))
        if min_price is not None:
            filters.append(Product.price >= min_price)
        if max_price is not None:
            filters.append(Product.price <= max_price)
        if min_rating is not None:
            filters.append(Product.avg_rating >= min_rating)
        if in_stock is True:
            filters.append(Product.stock_quantity > 0)

        # Flexible multi-word keyword search with synonyms, categories, and tags
        if q and q.strip():
            query = query.outerjoin(Category, Product.category_id == Category.id)
            count_query = count_query.outerjoin(Category, Product.category_id == Category.id)

            words = q.strip().split()
            word_filters = []
            for word in words:
                w_lower = word.lower()
                expanded_terms = SYNONYMS.get(w_lower, [w_lower])
                term_conditions = []
                for term in expanded_terms:
                    pat = f"%{term}%"
                    term_conditions.extend([
                        Product.title.ilike(pat),
                        Product.description.ilike(pat),
                        Product.brand.ilike(pat),
                        Product.short_description.ilike(pat),
                        Category.name.ilike(pat),
                        Category.slug.ilike(pat),
                        func.array_to_string(Product.tags, ' ').ilike(pat),
                    ])
                word_filters.append(or_(*term_conditions))
            filters.append(and_(*word_filters))

        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))

        # Sorting
        sort_column = {
            "created_at": Product.created_at.desc(),
            "price_asc": Product.price.asc(),
            "price_desc": Product.price.desc(),
            "rating": Product.avg_rating.desc(),
            "title": Product.title.asc(),
        }.get(sort_by, Product.created_at.desc())

        query = query.order_by(sort_column).offset(skip).limit(limit)

        result = await self.db.execute(query)
        products = list(result.scalars().unique().all())

        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        # Semantic Vector Search Fallback:
        # If keyword search returned zero products and the user passed a search query,
        # fallback seamlessly to vector semantic search!
        if total == 0 and q and q.strip():
            try:
                from app.services.vector_service import VectorService
                vec_service = VectorService(self.db)
                sem_results = await vec_service.semantic_search(
                    query=q,
                    limit=limit,
                    min_price=min_price,
                    max_price=max_price,
                    category_id=category_id,
                    category=category,
                )
                if sem_results:
                    products = [p for p, _ in sem_results]
                    total = len(products)
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Semantic fallback failed: {e}")

        return products, total

    async def get_by_id(self, product_id: uuid.UUID) -> Product:
        """Get a single product by ID with all relations loaded."""
        result = await self.db.execute(
            select(Product)
            .options(
                selectinload(Product.images),
                selectinload(Product.category),
            )
            .where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        return product

    async def get_by_slug(self, slug: str) -> Product:
        """Get a single product by slug."""
        result = await self.db.execute(
            select(Product)
            .options(
                selectinload(Product.images),
                selectinload(Product.category),
            )
            .where(Product.slug == slug)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        return product

    async def create(self, data: ProductCreate) -> Product:
        """Create a new product with auto-generated SKU and slug."""
        # Generate unique slug
        base_slug = slugify(data.title)
        slug = base_slug
        counter = 1
        while True:
            result = await self.db.execute(
                select(Product.id).where(Product.slug == slug)
            )
            if not result.scalar_one_or_none():
                break
            slug = f"{base_slug}-{counter}"
            counter += 1

        # Generate SKU
        sku = f"NM-{uuid.uuid4().hex[:8].upper()}"

        product = Product(
            sku=sku,
            slug=slug,
            **data.model_dump(),
        )
        self.db.add(product)
        await self.db.flush()
        return product

    async def update(self, product_id: uuid.UUID, data: ProductUpdate) -> Product:
        """Update an existing product."""
        product = await self.get_by_id(product_id)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        # Regenerate slug if title changed
        if "title" in update_data:
            product.slug = slugify(update_data["title"])

        await self.db.flush()
        return product

    async def delete(self, product_id: uuid.UUID) -> None:
        """Delete a product."""
        product = await self.get_by_id(product_id)
        await self.db.delete(product)
        await self.db.flush()
