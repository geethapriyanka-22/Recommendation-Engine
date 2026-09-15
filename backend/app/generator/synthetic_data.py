"""
NovaMart — Synthetic Data Generator

Master orchestrator that generates a complete, realistic e-commerce dataset:
categories, products, users, reviews, orders, addresses, and embeddings.
"""

import logging
import random
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from slugify import slugify
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.security import hash_password
from app.generator.product_templates import AUTHENTIC_PRODUCTS, ORIGINAL_CATEGORIES
from app.generator.review_templates import generate_review_text, pick_rating
from app.generator.user_templates import (
    CITIES,
    DEFAULT_ACCOUNTS,
    FIRST_NAMES,
    LAST_NAMES,
    STREET_NAMES,
    STREET_SUFFIXES,
)
from app.models.cart import Cart
from app.models.category import Category
from app.models.order import Address, Order, OrderItem, OrderStatus
from app.models.product import Product, ProductImage
from app.models.review import Review
from app.models.user import User, UserRole
from app.services.vector_service import VectorService

logger = logging.getLogger(__name__)


class SyntheticDataGenerator:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users: list[User] = []
        self.products: list[Product] = []
        self.categories: dict[str, Category] = {}

    async def generate_all(self) -> dict:
        """Run the full synthetic data generation pipeline."""
        logger.info("🚀 Starting synthetic data generation...")

        stats = {}

        # 1. Users
        stats["users"] = await self._generate_users()
        logger.info(f"  ✅ Generated {stats['users']} users")

        # 2. Addresses
        stats["addresses"] = await self._generate_addresses()
        logger.info(f"  ✅ Generated {stats['addresses']} addresses")

        # 3. Categories
        stats["categories"] = await self._generate_categories()
        logger.info(f"  ✅ Generated {stats['categories']} categories")

        # 4. Products
        stats["products"] = await self._generate_products()
        logger.info(f"  ✅ Generated {stats['products']} products")

        # 5. Reviews
        stats["reviews"] = await self._generate_reviews()
        logger.info(f"  ✅ Generated {stats['reviews']} reviews")

        # 6. Orders
        stats["orders"] = await self._generate_orders()
        logger.info(f"  ✅ Generated {stats['orders']} orders")

        # 7. Embeddings
        stats["embeddings"] = await self._generate_embeddings()
        logger.info(f"  ✅ Generated {stats['embeddings']} embeddings")

        logger.info("🎉 Synthetic data generation complete!")
        return stats

    async def _generate_users(self) -> int:
        """Generate default accounts + random customer accounts."""
        count = 0

        # Default accounts (admin, sellers, demo customer)
        for account in DEFAULT_ACCOUNTS:
            existing = await self.db.execute(
                select(User).where(User.email == account["email"])
            )
            if existing.scalar_one_or_none():
                continue

            user = User(
                email=account["email"],
                hashed_password=hash_password(account["password"]),
                full_name=account["full_name"],
                role=UserRole(account["role"]),
                is_active=True,
            )
            self.db.add(user)
            self.users.append(user)
            count += 1

        # Random customers
        used_emails = {a["email"] for a in DEFAULT_ACCOUNTS}
        for _ in range(25):
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            email = f"{first.lower()}.{last.lower()}{random.randint(1, 99)}@email.com"

            if email in used_emails:
                continue
            used_emails.add(email)

            user = User(
                email=email,
                hashed_password=hash_password("Password123!"),
                full_name=f"{first} {last}",
                role=UserRole.CUSTOMER,
                is_active=True,
            )
            self.db.add(user)
            self.users.append(user)
            count += 1

        await self.db.flush()

        # Reload all users
        result = await self.db.execute(select(User))
        self.users = list(result.scalars().all())

        return count

    async def _generate_addresses(self) -> int:
        """Generate 1-2 addresses per user."""
        count = 0
        for user in self.users:
            num_addresses = random.choices([1, 2], weights=[0.6, 0.4])[0]
            for i in range(num_addresses):
                city, state = random.choice(CITIES)
                street_num = random.randint(100, 9999)
                street_name = random.choice(STREET_NAMES)
                street_suffix = random.choice(STREET_SUFFIXES)

                address = Address(
                    user_id=user.id,
                    label="home" if i == 0 else "work",
                    full_name=user.full_name,
                    street_address=f"{street_num} {street_name} {street_suffix}",
                    city=city,
                    state=state,
                    postal_code=f"{random.randint(10000, 99999)}",
                    country="US",
                    is_default=i == 0,
                )
                self.db.add(address)
                count += 1

        await self.db.flush()
        return count

    async def wipe_database(self) -> None:
        """Wipe all existing records for a complete database reset."""
        logger.info("🧹 Wiping existing database records...")
        from sqlalchemy import text
        await self.db.execute(text("""
            TRUNCATE TABLE 
                product_embeddings, 
                product_images, 
                order_items, 
                orders, 
                cart_items, 
                carts, 
                reviews, 
                products, 
                categories, 
                addresses, 
                users 
            CASCADE;
        """))
        await self.db.flush()
        logger.info("  ✅ Database wiped clean.")

    async def _generate_categories(self) -> int:
        """Generate categories from authentic definitions (top-level + subcategories)."""
        count = 0
        sort_order = 0

        for cat_key, cat_data in ORIGINAL_CATEGORIES.items():
            # Top-level category
            parent = Category(
                name=cat_data["name"],
                slug=slugify(cat_key),
                description=cat_data["description"],
                icon=cat_data["icon"],
                sort_order=sort_order,
            )
            self.db.add(parent)
            await self.db.flush()
            self.categories[cat_key] = parent
            count += 1
            sort_order += 1

            # Subcategories
            for sub_name in cat_data["subcategories"]:
                child = Category(
                    name=sub_name,
                    slug=slugify(f"{cat_key}-{sub_name}"),
                    description=f"{sub_name} in {cat_data['name']}",
                    parent_id=parent.id,
                    sort_order=sort_order,
                )
                self.db.add(child)
                await self.db.flush()
                self.categories[f"{cat_key}:{sub_name}"] = child
                count += 1
                sort_order += 1

        return count

    async def _generate_products(self) -> int:
        """Generate authentic, recognizable real-world products with high-res photos."""
        count = 0

        for p_data in AUTHENTIC_PRODUCTS:
            cat_key = p_data["category"]
            sub_key = p_data.get("subcategory", "")
            category = self.categories.get(f"{cat_key}:{sub_key}") or self.categories.get(cat_key)

            title = p_data["title"]
            sku = f"NM-{uuid.uuid4().hex[:8].upper()}"
            slug = slugify(title)

            # Ensure slug uniqueness
            existing = await self.db.execute(
                select(Product.id).where(Product.slug == slug)
            )
            if existing.scalar_one_or_none():
                slug = f"{slug}-{uuid.uuid4().hex[:4]}"

            product = Product(
                sku=sku,
                title=title,
                slug=slug,
                description=p_data["description"],
                short_description=p_data["short_description"],
                price=Decimal(str(p_data["price"])),
                compare_at_price=Decimal(str(p_data["compare_at_price"])) if p_data.get("compare_at_price") else None,
                stock_quantity=p_data.get("stock", random.randint(20, 100)),
                category_id=category.id,
                brand=p_data["brand"],
                attributes=p_data.get("attributes", {}),
                tags=p_data.get("tags", []),
                is_published=True,
                is_featured=p_data.get("price", 0) > 1000 or "bestseller" in p_data.get("tags", []),
            )
            self.db.add(product)
            await self.db.flush()

            # Add product images
            for img_idx, img_url in enumerate(p_data.get("images", [])):
                image = ProductImage(
                    product_id=product.id,
                    url=img_url,
                    alt_text=f"{title} - View {img_idx + 1}",
                    sort_order=img_idx,
                )
                self.db.add(image)

            self.products.append(product)
            count += 1

        await self.db.flush()
        return count

    async def _generate_reviews(self) -> int:
        """Generate reviews with realistic J-curve rating distribution."""
        count = 0
        customers = [u for u in self.users if u.role == UserRole.CUSTOMER]

        if not customers:
            return 0

        for product in self.products:
            num_reviews = random.randint(1, 8)
            reviewers = random.sample(customers, min(num_reviews, len(customers)))

            total_rating = 0
            for user in reviewers:
                rating = pick_rating()
                review_data = generate_review_text(rating, product.title)

                review = Review(
                    product_id=product.id,
                    user_id=user.id,
                    rating=rating,
                    title=review_data["title"],
                    body=review_data["body"],
                    is_verified_purchase=random.random() < 0.6,
                )
                self.db.add(review)
                total_rating += rating
                count += 1

            # Update denormalized rating
            product.review_count = len(reviewers)
            product.avg_rating = round(total_rating / len(reviewers), 2)

        await self.db.flush()
        return count

    async def _generate_orders(self) -> int:
        """Generate realistic order history."""
        count = 0
        customers = [u for u in self.users if u.role == UserRole.CUSTOMER]

        if not customers or not self.products:
            return 0

        statuses = [
            OrderStatus.DELIVERED,
            OrderStatus.DELIVERED,
            OrderStatus.DELIVERED,
            OrderStatus.SHIPPED,
            OrderStatus.PROCESSING,
            OrderStatus.CONFIRMED,
            OrderStatus.PENDING,
            OrderStatus.CANCELLED,
        ]

        # Get addresses
        addr_result = await self.db.execute(select(Address))
        all_addresses = list(addr_result.scalars().all())
        addr_by_user = {}
        for addr in all_addresses:
            addr_by_user.setdefault(addr.user_id, []).append(addr)

        for customer in customers:
            num_orders = random.randint(1, 5)
            customer_addrs = addr_by_user.get(customer.id, [])

            for order_idx in range(num_orders):
                # Pick 1-4 random products
                order_products = random.sample(
                    self.products, min(random.randint(1, 4), len(self.products))
                )

                subtotal = Decimal("0.00")
                items_data = []

                for prod in order_products:
                    qty = random.randint(1, 3)
                    unit_price = Decimal(str(prod.price))
                    line_total = unit_price * qty
                    subtotal += line_total

                    items_data.append({
                        "product_id": prod.id,
                        "product_title": prod.title,
                        "product_sku": prod.sku,
                        "quantity": qty,
                        "unit_price": float(unit_price),
                        "total_price": float(line_total),
                    })

                tax = float(subtotal * Decimal("0.08"))
                total = float(subtotal) + tax

                # Random date in the last 6 months
                days_ago = random.randint(1, 180)
                created_at = datetime.now(timezone.utc) - timedelta(days=days_ago)

                order_number = f"ORD-{created_at.strftime('%Y%m%d')}-{count + 1:04d}"
                status = random.choice(statuses)

                addr_id = None
                if customer_addrs:
                    addr_id = random.choice(customer_addrs).id

                order = Order(
                    order_number=order_number,
                    user_id=customer.id,
                    status=status,
                    shipping_address_id=addr_id,
                    subtotal=float(subtotal),
                    tax_amount=tax,
                    total=total,
                )
                order.created_at = created_at
                self.db.add(order)
                await self.db.flush()

                for item_data in items_data:
                    order_item = OrderItem(order_id=order.id, **item_data)
                    self.db.add(order_item)

                count += 1

        await self.db.flush()
        return count

    async def _generate_embeddings(self) -> int:
        """Generate vector embeddings for all products."""
        # Reload products with categories
        result = await self.db.execute(
            select(Product).options(selectinload(Product.category))
        )
        products = list(result.scalars().all())

        vector_service = VectorService(self.db)
        count = await vector_service.bulk_generate_embeddings(products)
        return count
