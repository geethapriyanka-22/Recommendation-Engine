"""
NovaMart — Product, ProductImage, ProductEmbedding Models

Core product catalog with JSONB attributes, array tags,
image gallery, and pgvector embeddings for semantic search.
"""

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pgvector.sqlalchemy import Vector

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Product(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price > 0", name="ck_products_price_positive"),
        CheckConstraint("stock_quantity >= 0", name="ck_products_stock_non_negative"),
        CheckConstraint(
            "compare_at_price IS NULL OR compare_at_price > price",
            name="ck_products_compare_price",
        ),
    )

    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    slug: Mapped[str] = mapped_column(String(350), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    short_description: Mapped[str] = mapped_column(String(500), nullable=False)

    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    compare_at_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)

    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    category_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )
    brand: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)

    attributes: Mapped[dict] = mapped_column(JSONB, default=dict, server_default="{}")
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, server_default="{}")

    avg_rating: Mapped[float] = mapped_column(Numeric(3, 2), default=0.00)
    review_count: Mapped[int] = mapped_column(Integer, default=0)

    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)

    # ─── Relationships ───────────────────────────────────
    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan", order_by="ProductImage.sort_order")
    embedding = relationship("ProductEmbedding", back_populates="product", uselist=False, cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self) -> str:
        return f"<Product {self.sku}: {self.title[:40]}>"


class ProductImage(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "product_images"

    product_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    alt_text: Mapped[str | None] = mapped_column(String(200), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # ─── Relationships ───────────────────────────────────
    product = relationship("Product", back_populates="images")


class ProductEmbedding(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "product_embeddings"

    product_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    embedding = mapped_column(Vector(384), nullable=False)
    embedding_model: Mapped[str] = mapped_column(String(100), nullable=False)
    embedding_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
    )

    # ─── Relationships ───────────────────────────────────
    product = relationship("Product", back_populates="embedding")
