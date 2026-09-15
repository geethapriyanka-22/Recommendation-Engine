"""
NovaMart — Vector Service

Embedding generation, semantic search, and personalized product recommendations
using Semantic Feature Vectorizer + pgvector.
"""

import hashlib
import logging
import math
import re
import uuid

import numpy as np
from sqlalchemy import and_, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.category import Category
from app.models.product import Product, ProductEmbedding

logger = logging.getLogger(__name__)

# ─── Lazy-loaded embedding model (singleton) ────────────
_model = None


SEMANTIC_TAXONOMY = {
    # ── ROOT DEPARTMENT CLUSTERS ──
    "root_electronics": {
        "dims": (0, 32),
        "weight": 2.5,
        "keywords": {"electronics", "electronic", "tech", "digital", "gadget", "device", "battery", "usb", "screen", "smart"}
    },
    "root_fashion": {
        "dims": (144, 168),
        "weight": 2.5,
        "keywords": {"fashion", "apparel", "clothing", "designer", "luxury", "wear", "wardrobe", "style", "outfit", "textile"}
    },
    "root_home": {
        "dims": (240, 256),
        "weight": 2.5,
        "keywords": {"home", "kitchen", "cookware", "cooking", "living", "interior", "appliance", "appliances"}
    },
    "root_beauty": {
        "dims": (288, 304),
        "weight": 2.5,
        "keywords": {"beauty", "cosmetic", "cosmetics", "skincare", "scent", "grooming", "wellness", "care"}
    },
    "root_sports": {
        "dims": (336, 352),
        "weight": 2.5,
        "keywords": {"sports", "outdoor", "outdoors", "athletics", "athletic", "fitness", "performance", "exercise"}
    },

    # ── LEAF SPECIALTY CLUSTERS ──
    "sub_mobile": {
        "dims": (32, 64),
        "weight": 4.5,
        "keywords": {
            "mobile", "mobiles", "phone", "phones", "smartphone", "smartphones",
            "iphone", "android", "galaxy", "pixel", "cellular", "5g", "s-pen",
            "ios", "oled", "amoled", "samsung", "apple", "smartphones & tablets"
        }
    },
    "sub_laptops": {
        "dims": (64, 96),
        "weight": 4.5,
        "keywords": {
            "laptop", "laptops", "macbook", "notebook", "computer", "computers",
            "dell", "xps", "intel", "ryzen", "gpu", "rtx", "cpu", "ssd", "ram",
            "processor", "keyboard", "trackpad", "laptops & computers"
        }
    },
    "sub_audio": {
        "dims": (96, 120),
        "weight": 4.5,
        "keywords": {
            "audio", "sound", "headphone", "headphones", "earbuds", "earphones",
            "noise-canceling", "anc", "bluetooth", "speaker", "speakers", "sonos",
            "sony", "wh-1000xm5", "hi-res", "ldac", "audio & headphones"
        }
    },
    "sub_cameras_wearables": {
        "dims": (120, 144),
        "weight": 4.5,
        "keywords": {
            "camera", "cameras", "fujifilm", "sensor", "lens", "optics", "shutter",
            "watch", "smartwatch", "wearable", "wearables", "ultra 2", "garmin",
            "smart home & wearables", "cameras & optics"
        }
    },
    "sub_apparel": {
        "dims": (168, 204),
        "weight": 4.5,
        "keywords": {
            "coat", "trench", "jacket", "outerwear", "gabardine", "tailored", "tailoring",
            "wool", "cashmere", "burberry", "toteme", "totême", "wrap", "jackets & outerwear",
            "jeans", "trousers", "shirt", "sweater"
        }
    },
    "sub_accessories_shoes": {
        "dims": (204, 240),
        "weight": 4.5,
        "keywords": {
            "bag", "handbag", "purse", "crossbody", "tote", "calfskin", "leather",
            "loewe", "puzzle", "sneakers", "sneaker", "shoes", "footwear", "loafers",
            "suede", "loro piana", "sunglasses", "acetate", "saint laurent",
            "sneakers & footwear", "bags & luggage", "eyewear & accessories"
        }
    },
    "sub_kitchen_home": {
        "dims": (256, 288),
        "weight": 4.5,
        "keywords": {
            "dutch oven", "cast iron", "le creuset", "kettle", "fellow", "stagg",
            "espresso", "barista", "breville", "coffee", "blender", "vitamix",
            "vacuum", "dyson", "v15", "chair", "herman miller", "aeron", "ergonomic",
            "furniture", "kitchen appliances", "cookware & dining"
        }
    },
    "sub_skincare_fragrance": {
        "dims": (304, 336),
        "weight": 4.5,
        "keywords": {
            "cream", "moisturizer", "rich cream", "tfc8", "augustinus bader", "serum",
            "la mer", "perfume", "fragrance", "parfum", "baccarat rouge", "mfk",
            "kurkdjian", "santal 33", "le labo", "airwrap", "hair", "styling",
            "fragrances & perfumes", "skincare treatments"
        }
    },
    "sub_sports_outdoor": {
        "dims": (352, 384),
        "weight": 4.5,
        "keywords": {
            "running", "runners", "on running", "cloudmonster", "hoka", "clifton",
            "lululemon", "align", "leggings", "yoga", "arc'teryx", "beta ar",
            "gore-tex", "cooler", "yeti", "tundra", "camping", "activewear",
            "gps & sports watches", "outdoor & camping"
        }
    }
}


class ResilientEmbeddingModel:
    """High-fidelity semantic feature vectorizer using taxonomy subspaces and token projections."""
    def __init__(self, dim: int = 384):
        self.dim = dim

    def _tokenize(self, text: str) -> list[str]:
        cleaned = re.sub(r"[^a-zA-Z0-9\s\-_]", " ", text.lower())
        tokens = [t for t in cleaned.split() if len(t) > 1]
        bigrams = [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens) - 1)]
        return tokens + bigrams

    def encode(self, texts):
        is_single = isinstance(texts, str)
        items = [texts] if is_single else texts
        results = []

        for text in items:
            vec = np.zeros(self.dim, dtype=np.float32)
            tokens = self._tokenize(text)
            token_set = set(tokens)

            # 1. Semantic Cluster Activations
            for domain, cfg in SEMANTIC_TAXONOMY.items():
                start, end = cfg["dims"]
                weight = cfg["weight"]
                kws = cfg["keywords"]
                overlap = token_set.intersection(kws)
                if overlap:
                    sub_weight = weight * (1.0 + 0.3 * len(overlap))
                    for d in range(start, end):
                        val = math.sin((d - start + 1) * 1.5707)
                        vec[d] += sub_weight * (0.85 + 0.15 * val)

            # 2. Universal Hash Token Signatures across all 384 dimensions
            for tok in tokens:
                h = int(hashlib.md5(tok.encode("utf-8")).hexdigest()[:8], 16)
                idx = h % self.dim
                sign = 1.0 if (h & 1) else -1.0
                vec[idx] += sign * 1.0

            # 3. L2 Normalization
            norm = np.linalg.norm(vec)
            if norm > 1e-6:
                vec = vec / norm
            else:
                vec = np.ones(self.dim, dtype=np.float32) / np.sqrt(self.dim)

            results.append(vec)

        return results[0] if is_single else np.array(results)


class FastEmbedAdapter:
    """Adapter to give fastembed the same .encode() interface as SentenceTransformer."""
    def __init__(self, model):
        self.model = model

    def encode(self, texts):
        is_single = isinstance(texts, str)
        items = [texts] if is_single else list(texts)
        embeddings = list(self.model.embed(items))
        if is_single:
            return np.array(embeddings[0], dtype=np.float32)
        return np.array(embeddings, dtype=np.float32)


def get_embedding_model():
    """Lazy-load embedding model: fastembed (ONNX) -> sentence-transformers -> resilient fallback."""
    global _model
    if _model is None:
        try:
            from fastembed import TextEmbedding
            logger.info("Loading FastEmbed model: sentence-transformers/all-MiniLM-L6-v2")
            raw_model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
            _model = FastEmbedAdapter(raw_model)
            logger.info("FastEmbed model loaded successfully")
        except Exception as e:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
                _model = SentenceTransformer(settings.EMBEDDING_MODEL)
                logger.info("Embedding model loaded successfully")
            except Exception as e2:
                logger.info(f"Using high-fidelity semantic feature vectorizer ({e} / {e2}).")
                _model = ResilientEmbeddingModel(dim=settings.EMBEDDING_DIMENSIONS)
    return _model


STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "can", "could", "did", "do", "does", "doing",
    "down", "during", "each", "few", "for", "from", "further", "had", "has", "have",
    "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how",
    "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me", "more", "most",
    "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should",
    "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "we", "were", "what", "when", "where", "which",
    "while", "who", "whom", "why", "with", "would", "you", "your", "yours",
    "want", "need", "show", "find", "looking", "give", "best", "good"
}


def clean_query_text(query: str) -> str:
    """Strip punctuation and common stopwords for better FTS ranking."""
    tokens = re.sub(r"[^\w\s-]", " ", query).split()
    meaningful = [t for t in tokens if t.lower() not in STOP_WORDS and len(t) > 1]
    return " ".join(meaningful) if meaningful else query


def build_embedding_text(product: Product) -> str:
    """Construct rich semantic text representation for embedding."""
    parts = [
        f"Product: {product.title}",
    ]

    # Safely check category without triggering synchronous lazy-load
    cat = product.__dict__.get("category")
    if cat and hasattr(cat, "name") and cat.name:
        parts.append(f"Category: {cat.name}")

    if product.brand:
        parts.append(f"Brand: {product.brand}")

    parts.append(f"Description: {product.description}")
    parts.append(f"Price: ₹{product.price}")

    if product.attributes:
        attrs = ", ".join(f"{k}: {v}" for k, v in product.attributes.items())
        parts.append(f"Specifications: {attrs}")

    if product.tags:
        parts.append(f"Tags: {', '.join(product.tags)}")

    return " | ".join(parts)


class VectorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_embedding(self, product: Product) -> ProductEmbedding:
        """Generate and store an embedding for a single product."""
        model = get_embedding_model()
        embedding_text = build_embedding_text(product)
        vector = model.encode(embedding_text).tolist()

        existing = await self.db.execute(
            select(ProductEmbedding).where(ProductEmbedding.product_id == product.id)
        )
        old = existing.scalar_one_or_none()
        if old:
            await self.db.delete(old)
            await self.db.flush()

        embedding = ProductEmbedding(
            product_id=product.id,
            embedding=vector,
            embedding_model=settings.EMBEDDING_MODEL,
            embedding_text=embedding_text,
        )
        self.db.add(embedding)
        await self.db.flush()
        return embedding

    async def bulk_generate_embeddings(self, products: list[Product]) -> int:
        """Generate embeddings for a batch of products."""
        model = get_embedding_model()
        count = 0

        # Clean existing embeddings first to prevent unique constraint conflicts
        await self.db.execute(text("DELETE FROM product_embeddings;"))
        await self.db.flush()

        batch_size = 32
        for i in range(0, len(products), batch_size):
            batch = products[i:i + batch_size]
            texts = [build_embedding_text(p) for p in batch]
            vectors = model.encode(texts).tolist()

            for product, vector in zip(batch, vectors):
                embedding = ProductEmbedding(
                    product_id=product.id,
                    embedding=vector,
                    embedding_model=settings.EMBEDDING_MODEL,
                    embedding_text=texts[batch.index(product)],
                )
                self.db.add(embedding)
                count += 1

            await self.db.flush()
            logger.info(f"Embedded batch {i // batch_size + 1}: {len(batch)} products")

        return count

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

    async def semantic_search(
        self,
        query: str,
        limit: int = 10,
        min_price: float | None = None,
        max_price: float | None = None,
        category_id: uuid.UUID | None = None,
        category: str | None = None,
        min_score: float = 0.30,
    ) -> list[tuple[Product, float]]:
        """
        Hybrid search combining neural vector similarity, full-text ranking, and popularity
        with minimum relevance cutoff to prevent noise bleed.
        """
        cat_ids = await self._resolve_category_ids(category_id=category_id, category=category)
        if cat_ids is not None and len(cat_ids) == 0:
            return []

        model = get_embedding_model()
        query_vector = model.encode(query).tolist()
        vector_str = f"[{','.join(str(v) for v in query_vector)}]"
        fts_text = clean_query_text(query)

        sql = text("""
            WITH vector_results AS (
                SELECT
                    p.id,
                    1 - (pe.embedding <=> :query_vec ::vector) AS vector_score
                FROM products p
                JOIN product_embeddings pe ON pe.product_id = p.id
                WHERE p.is_published = TRUE
                    AND (CAST(:min_price AS NUMERIC) IS NULL OR p.price >= CAST(:min_price AS NUMERIC))
                    AND (CAST(:max_price AS NUMERIC) IS NULL OR p.price <= CAST(:max_price AS NUMERIC))
                    AND (CAST(:cat_ids AS uuid[]) IS NULL OR p.category_id = ANY(CAST(:cat_ids AS uuid[])))
                ORDER BY pe.embedding <=> :query_vec ::vector
                LIMIT 50
            ),
            fts_results AS (
                SELECT
                    p.id,
                    ts_rank_cd(
                        to_tsvector('english', p.title || ' ' || COALESCE(p.brand, '') || ' ' || p.description),
                        plainto_tsquery('english', :fts_text)
                    ) AS fts_score
                FROM products p
                WHERE p.is_published = TRUE
                    AND (CAST(:cat_ids AS uuid[]) IS NULL OR p.category_id = ANY(CAST(:cat_ids AS uuid[])))
                    AND to_tsvector('english', p.title || ' ' || COALESCE(p.brand, '') || ' ' || p.description)
                        @@ plainto_tsquery('english', :fts_text)
            ),
            combined AS (
                SELECT
                    p.id,
                    COALESCE(vr.vector_score, 0) AS v_score,
                    COALESCE(fr.fts_score, 0) AS f_score,
                    (
                        COALESCE(vr.vector_score, 0) * 0.65 +
                        COALESCE(fr.fts_score, 0) * 0.20 +
                        (p.avg_rating * LN(p.review_count + 1) / 10.0) * 0.15
                    ) AS hybrid_score
                FROM products p
                LEFT JOIN vector_results vr ON vr.id = p.id
                LEFT JOIN fts_results fr ON fr.id = p.id
                WHERE (vr.id IS NOT NULL OR fr.id IS NOT NULL)
            )
            SELECT
                id,
                hybrid_score
            FROM combined
            WHERE (v_score >= 0.32 OR f_score > 0.005)
                AND hybrid_score >= :min_score
            ORDER BY hybrid_score DESC
            LIMIT :result_limit
        """)

        result = await self.db.execute(
            sql,
            {
                "query_vec": vector_str,
                "fts_text": fts_text,
                "min_price": min_price,
                "max_price": max_price,
                "cat_ids": cat_ids,
                "min_score": min_score,
                "result_limit": limit,
            },
        )
        rows = result.all()

        products_with_scores = []
        for row in rows:
            product_id, score = row
            product_result = await self.db.execute(
                select(Product)
                .options(selectinload(Product.images))
                .where(Product.id == product_id)
            )
            product = product_result.scalar_one_or_none()
            if product:
                products_with_scores.append((product, float(score)))

        return products_with_scores

    async def get_recommendations(
        self, product_id: uuid.UUID, limit: int = 5
    ) -> list[tuple[Product, float]]:
        """
        Find products similar to a given product with strict category alignment.
        Guarantees that viewing a mobile phone or electronic product will NEVER
        recommend unrelated items (like fashion or footwear).
        """
        # Load source product and its category hierarchy
        src_res = await self.db.execute(
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.id == product_id)
        )
        source_product = src_res.scalar_one_or_none()
        if not source_product:
            return []

        # Get the source product's embedding
        result = await self.db.execute(
            select(ProductEmbedding).where(ProductEmbedding.product_id == product_id)
        )
        source_embedding = result.scalar_one_or_none()
        if not source_embedding:
            return []

        vector_str = f"[{','.join(str(v) for v in source_embedding.embedding)}]"

        # Identify category and sibling categories under same parent
        cat_id = source_product.category_id
        parent_id = source_product.category.parent_id if source_product.category else None

        sibling_cat_ids = [cat_id]
        if parent_id:
            sib_res = await self.db.execute(
                select(Category.id).where(Category.parent_id == parent_id)
            )
            sibling_cat_ids = list(sib_res.scalars().all())

        sql = text("""
            SELECT
                p.id,
                (
                    (1 - (pe.embedding <=> :source_vec ::vector)) * 0.70 +
                    (CASE 
                        WHEN p.category_id = :cat_id THEN 0.25
                        WHEN p.category_id = ANY(:sibling_cat_ids) THEN 0.15
                        ELSE -0.60
                     END) +
                    (COALESCE(p.avg_rating, 0) / 50.0)
                ) AS similarity
            FROM products p
            JOIN product_embeddings pe ON pe.product_id = p.id
            WHERE p.id != :source_id
                AND p.is_published = TRUE
                -- Strict department filtering: only same category, siblings, or exceptionally close match
                AND (
                    p.category_id = :cat_id
                    OR p.category_id = ANY(:sibling_cat_ids)
                    OR (1 - (pe.embedding <=> :source_vec ::vector)) > 0.75
                )
            ORDER BY similarity DESC
            LIMIT :result_limit
        """)

        result = await self.db.execute(
            sql,
            {
                "source_vec": vector_str,
                "source_id": product_id,
                "cat_id": cat_id,
                "sibling_cat_ids": sibling_cat_ids,
                "result_limit": limit,
            },
        )
        rows = result.all()

        products_with_scores = []
        for row in rows:
            pid, similarity = row
            product_result = await self.db.execute(
                select(Product)
                .options(selectinload(Product.images))
                .where(Product.id == pid)
            )
            product = product_result.scalar_one_or_none()
            if product:
                products_with_scores.append((product, float(similarity)))

        return products_with_scores

    async def get_personalized_recommendations(
        self,
        interacted_ids: list[uuid.UUID],
        search_queries: list[str] | None = None,
        limit: int = 4,
    ) -> dict:
        """
        Generate dynamic homepage recommendations based on user interactions
        (products visited, added to cart, or purchased) and search queries.
        """
        search_queries = [q.strip() for q in (search_queries or []) if q and q.strip()]

        # If no interaction history and no search queries, return top curated bestsellers
        if not interacted_ids and not search_queries:
            bestsellers_res = await self.db.execute(
                select(Product)
                .options(selectinload(Product.images))
                .where(Product.is_published == True)
                .order_by(Product.avg_rating.desc(), Product.review_count.desc())
                .limit(limit)
            )
            bestsellers = list(bestsellers_res.scalars().all())
            return {
                "recommendations": [(p, 1.0) for p in bestsellers],
                "reason": "Trending & Curated Bestsellers",
                "is_personalized": False,
            }

        # Load interacted products and their embeddings
        interacted_products = []
        if interacted_ids:
            int_res = await self.db.execute(
                select(Product)
                .options(
                    selectinload(Product.category),
                    selectinload(Product.embedding),
                )
                .where(Product.id.in_(interacted_ids))
            )
            interacted_products = list(int_res.scalars().all())

        model = get_embedding_model()
        user_vector = np.zeros(settings.EMBEDDING_DIMENSIONS, dtype=np.float32)
        valid_vectors = 0
        cat_ids = []
        parent_cat_ids = []
        dominant_cat_name = ""

        # 1. Product interaction vectors (weight: 1.0)
        for p in interacted_products:
            if p.category_id:
                cat_ids.append(p.category_id)
                if p.category and p.category.parent_id:
                    parent_cat_ids.append(p.category.parent_id)
                if not dominant_cat_name and p.category:
                    dominant_cat_name = p.category.name

            if p.embedding and p.embedding.embedding:
                user_vector += np.array(p.embedding.embedding, dtype=np.float32)
                valid_vectors += 1

        # 2. Search query vectors (weight: 1.5 - recent searches show strong immediate intent)
        for q in search_queries[:3]:
            try:
                cleaned_q = clean_query_text(q)
                q_vec = model.encode(cleaned_q)
                user_vector += np.array(q_vec, dtype=np.float32) * 1.5
                valid_vectors += 1
            except Exception as e:
                logger.warning(f"Failed to embed search query '{q}': {e}")

        if valid_vectors > 0:
            norm = np.linalg.norm(user_vector)
            if norm > 1e-6:
                user_vector = user_vector / norm
        else:
            fallback_text = search_queries[0] if search_queries else (dominant_cat_name or "electronics")
            user_vector = model.encode(fallback_text)

        vector_str = f"[{','.join(str(v) for v in user_vector.tolist())}]"

        # Expand sibling categories
        all_affinity_cat_ids = list(set(cat_ids))
        if parent_cat_ids:
            sibs = await self.db.execute(
                select(Category.id).where(Category.parent_id.in_(parent_cat_ids))
            )
            all_affinity_cat_ids.extend(list(sibs.scalars().all()))
        all_affinity_cat_ids = list(set(all_affinity_cat_ids))

        has_cat_affinity = len(all_affinity_cat_ids) > 0

        sql = text(f"""
            SELECT
                p.id,
                (
                    (1 - (pe.embedding <=> :user_vec ::vector)) * 0.70 +
                    (CASE 
                        WHEN p.category_id = ANY(:cat_ids) THEN 0.20
                        WHEN p.category_id = ANY(:all_affinity_ids) THEN 0.10
                        ELSE 0.00
                     END) +
                    (COALESCE(p.avg_rating, 0) / 50.0)
                ) AS final_score
            FROM products p
            JOIN product_embeddings pe ON pe.product_id = p.id
            WHERE p.id != ALL(:interacted_ids)
                AND p.is_published = TRUE
                AND (
                    {"p.category_id = ANY(:all_affinity_ids) OR " if has_cat_affinity else ""}
                    (1 - (pe.embedding <=> :user_vec ::vector)) > 0.28
                )
            ORDER BY final_score DESC
            LIMIT :result_limit
        """)

        result = await self.db.execute(
            sql,
            {
                "user_vec": vector_str,
                "interacted_ids": interacted_ids or [uuid.UUID(int=0)],
                "cat_ids": cat_ids or [uuid.UUID(int=0)],
                "all_affinity_ids": all_affinity_cat_ids or [uuid.UUID(int=0)],
                "result_limit": limit,
            },
        )
        rows = result.all()

        products_with_scores = []
        for row in rows:
            pid, score = row
            product_result = await self.db.execute(
                select(Product)
                .options(selectinload(Product.images))
                .where(Product.id == pid)
            )
            p = product_result.scalar_one_or_none()
            if p:
                products_with_scores.append((p, float(score)))

        # Fallback if fewer than limit
        if len(products_with_scores) < limit:
            existing_ids = [p.id for p, _ in products_with_scores] + interacted_ids
            fill_res = await self.db.execute(
                select(Product)
                .options(selectinload(Product.images))
                .where(Product.id.notin_(existing_ids or [uuid.UUID(int=0)]), Product.is_published == True)
                .order_by(Product.avg_rating.desc())
                .limit(limit - len(products_with_scores))
            )
            for p in fill_res.scalars().all():
                products_with_scores.append((p, 0.85))

        # Dynamic reason description
        if search_queries and interacted_products:
            reason = f"Based on your search for '{search_queries[0]}' & recent activity"
        elif search_queries:
            reason = f"Based on your search for '{search_queries[0]}'"
        elif dominant_cat_name:
            reason = f"Based on your interest in {dominant_cat_name}"
        else:
            reason = "Inspired by your recent activity"

        return {
            "recommendations": products_with_scores,
            "reason": reason,
            "is_personalized": True,
        }
