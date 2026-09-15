"""
NovaMart — Unified Models Registry
Imports all models to ensure Declarative relationships are always registered.
"""

from app.models.base import Base
from app.models.user import User, UserRole
from app.models.category import Category
from app.models.product import Product, ProductImage, ProductEmbedding
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem, Address, OrderStatus
from app.models.review import Review

__all__ = [
    "Base",
    "User",
    "UserRole",
    "Category",
    "Product",
    "ProductImage",
    "ProductEmbedding",
    "Cart",
    "CartItem",
    "Order",
    "OrderItem",
    "Address",
    "OrderStatus",
    "Review",
]
