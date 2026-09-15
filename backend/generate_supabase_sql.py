import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import async_session_factory, engine
from app.models.base import Base
import app.models
from sqlalchemy import text
from sqlalchemy.schema import CreateTable

def esc(val):
    if val is None:
        return 'NULL'
    return "'" + str(val).replace("'", "''") + "'"

async def generate():
    sql_lines = []
    sql_lines.append('-- ========================================================')
    sql_lines.append('-- NovaMart: Complete Supabase Schema & Initial Data Dump')
    sql_lines.append('-- Open Supabase -> SQL Editor -> New Query -> Paste & Run')
    sql_lines.append('-- ========================================================\n')

    # 1. Clean Drop existing tables and types to avoid conflicts
    sql_lines.append('-- 1. Clean reset of existing tables and types')
    sql_lines.append('DROP TABLE IF EXISTS reviews, order_items, orders, cart_items, carts, product_embeddings, product_images, products, categories, addresses, users CASCADE;')
    sql_lines.append('DROP TYPE IF EXISTS user_role CASCADE;')
    sql_lines.append('DROP TYPE IF EXISTS order_status CASCADE;\n')

    # 2. Required PostgreSQL Extensions
    sql_lines.append('-- 2. Extensions')
    sql_lines.append('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    sql_lines.append('CREATE EXTENSION IF NOT EXISTS "vector";')
    sql_lines.append('CREATE EXTENSION IF NOT EXISTS "pg_trgm";\n')

    # 3. Enum Types (supporting both lowercase and uppercase to prevent any mismatch)
    sql_lines.append('-- 3. Custom Enum Types')
    sql_lines.append("CREATE TYPE user_role AS ENUM ('customer', 'seller', 'admin', 'CUSTOMER', 'SELLER', 'ADMIN');")
    sql_lines.append("CREATE TYPE order_status AS ENUM ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded', 'PENDING', 'CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'REFUNDED');\n")

    # 4. Table Schemas
    sql_lines.append('-- 4. Table Definitions')
    tables = [
        'users', 'addresses', 'categories', 'products', 'product_images',
        'product_embeddings', 'carts', 'cart_items', 'orders', 'order_items', 'reviews'
    ]
    
    for table_name in tables:
        table = Base.metadata.tables.get(table_name)
        if table is not None:
            stmt = str(CreateTable(table).compile(engine.sync_engine)).strip()
            stmt = stmt.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
            sql_lines.append(f'{stmt};\n')

    # 5. Data Inserts
    sql_lines.append('-- 5. Initial Data Inserts')
    async with async_session_factory() as session:
        # Users (inserted first because addresses, carts, orders, reviews reference users)
        users = (await session.execute(text('SELECT id, email, hashed_password, full_name, role, is_active FROM users;'))).all()
        for r in users:
            name = str(r[3]).replace("'", "''")
            role_val = str(r[4]).lower()
            sql_lines.append(f"INSERT INTO users (id, email, hashed_password, full_name, role, is_active) VALUES ('{r[0]}', '{r[1]}', '{r[2]}', '{name}', '{role_val}', {r[5]}) ON CONFLICT (id) DO NOTHING;")
        sql_lines.append('')

        # Addresses
        addresses = (await session.execute(text('SELECT id, user_id, label, full_name, street_address, city, state, postal_code, country, is_default FROM addresses;'))).all()
        for r in addresses:
            lbl = str(r[2]).replace("'", "''")
            fn = str(r[3]).replace("'", "''")
            sa = str(r[4]).replace("'", "''")
            ct = str(r[5]).replace("'", "''")
            st = str(r[6]).replace("'", "''")
            pc = str(r[7]).replace("'", "''")
            co = str(r[8]).replace("'", "''")
            sql_lines.append(f"INSERT INTO addresses (id, user_id, label, full_name, street_address, city, state, postal_code, country, is_default) VALUES ('{r[0]}', '{r[1]}', '{lbl}', '{fn}', '{sa}', '{ct}', '{st}', '{pc}', '{co}', {r[9]}) ON CONFLICT (id) DO NOTHING;")
        sql_lines.append('')

        # Categories (ordered so parent categories are inserted before subcategories)
        cats = (await session.execute(text('SELECT id, name, slug, description, icon, parent_id, sort_order FROM categories ORDER BY (parent_id IS NOT NULL), sort_order;'))).all()
        for r in cats:
            p_id = esc(r[5])
            desc = esc(r[3])
            icon = esc(r[4])
            name = str(r[1]).replace("'", "''")
            sql_lines.append(f"INSERT INTO categories (id, name, slug, description, icon, parent_id, sort_order) VALUES ('{r[0]}', '{name}', '{r[2]}', {desc}, {icon}, {p_id}, {r[6]}) ON CONFLICT (id) DO NOTHING;")
        sql_lines.append('')

        # Products
        prods = (await session.execute(text('SELECT id, sku, title, slug, description, short_description, price, compare_at_price, stock_quantity, category_id, brand, attributes, tags, avg_rating, review_count, is_published, is_featured FROM products;'))).all()
        for r in prods:
            comp_price = str(r[7]) if r[7] is not None else 'NULL'
            attrs = json.dumps(r[11] or {}).replace("'", "''")
            title = str(r[2]).replace("'", "''")
            desc = str(r[4]).replace("'", "''")
            short_desc = str(r[5]).replace("'", "''")
            brand = str(r[10]).replace("'", "''") if r[10] else ''
            tags = r[12] or []
            tag_sql = "ARRAY[" + ", ".join(["'" + t.replace("'", "''") + "'" for t in tags]) + "]::varchar[]" if tags else "ARRAY[]::varchar[]"
            sql_lines.append(f"INSERT INTO products (id, sku, title, slug, description, short_description, price, compare_at_price, stock_quantity, category_id, brand, attributes, tags, avg_rating, review_count, is_published, is_featured) VALUES ('{r[0]}', '{r[1]}', '{title}', '{r[3]}', '{desc}', '{short_desc}', {r[6]}, {comp_price}, {r[8]}, '{r[9]}', '{brand}', '{attrs}'::jsonb, {tag_sql}, {r[13]}, {r[14]}, {r[15]}, {r[16]}) ON CONFLICT (id) DO NOTHING;")
        sql_lines.append('')

        # Images
        imgs = (await session.execute(text('SELECT id, product_id, url, alt_text, sort_order FROM product_images;'))).all()
        for r in imgs:
            alt = str(r[3]).replace("'", "''") if r[3] else ''
            sql_lines.append(f"INSERT INTO product_images (id, product_id, url, alt_text, sort_order) VALUES ('{r[0]}', '{r[1]}', '{r[2]}', '{alt}', {r[4]}) ON CONFLICT (id) DO NOTHING;")
        sql_lines.append('')

        # Embeddings
        embs = (await session.execute(text('SELECT id, product_id, embedding, embedding_model, embedding_text FROM product_embeddings;'))).all()
        for r in embs:
            emb_text = str(r[4]).replace("'", "''") if r[4] else ''
            sql_lines.append(f"INSERT INTO product_embeddings (id, product_id, embedding, embedding_model, embedding_text) VALUES ('{r[0]}', '{r[1]}', '{r[2]}'::vector, '{r[3]}', '{emb_text}') ON CONFLICT (id) DO NOTHING;")
        sql_lines.append('')

        # Reviews
        reviews = (await session.execute(text('SELECT id, product_id, user_id, rating, title, body, is_verified_purchase, created_at FROM reviews;'))).all()
        for r in reviews:
            title = esc(r[4])
            body = esc(r[5])
            sql_lines.append(f"INSERT INTO reviews (id, product_id, user_id, rating, title, body, is_verified_purchase, created_at) VALUES ('{r[0]}', '{r[1]}', '{r[2]}', {r[3]}, {title}, {body}, {r[6]}, '{r[7]}') ON CONFLICT (id) DO NOTHING;")
        sql_lines.append('')

        # Orders
        orders = (await session.execute(text('SELECT id, order_number, user_id, status, shipping_address_id, subtotal, tax_amount, total, notes, created_at, updated_at FROM orders;'))).all()
        for r in orders:
            ship_id = esc(r[4])
            notes = esc(r[8])
            status_val = str(r[3]).lower()
            sql_lines.append(f"INSERT INTO orders (id, order_number, user_id, status, shipping_address_id, subtotal, tax_amount, total, notes, created_at, updated_at) VALUES ('{r[0]}', '{r[1]}', '{r[2]}', '{status_val}', {ship_id}, {r[5]}, {r[6]}, {r[7]}, {notes}, '{r[9]}', '{r[10]}') ON CONFLICT (id) DO NOTHING;")
        sql_lines.append('')

        # Order Items
        items = (await session.execute(text('SELECT id, order_id, product_id, product_title, product_sku, quantity, unit_price, total_price FROM order_items;'))).all()
        for r in items:
            pt = str(r[3]).replace("'", "''")
            ps = str(r[4]).replace("'", "''")
            sql_lines.append(f"INSERT INTO order_items (id, order_id, product_id, product_title, product_sku, quantity, unit_price, total_price) VALUES ('{r[0]}', '{r[1]}', '{r[2]}', '{pt}', '{ps}', {r[5]}, {r[6]}, {r[7]}) ON CONFLICT (id) DO NOTHING;")

    out_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'supabase_setup.sql')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_lines))
    print(f"SUCCESS: Generated {out_file} with {len(sql_lines)} SQL lines!")

if __name__ == '__main__':
    asyncio.run(generate())

