import re
import math
import hashlib
import numpy as np

SEMANTIC_TAXONOMY = {
    # ── ROOT CLUSTERS ──
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

    # ── LEAF CLUSTERS ──
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

class SemanticFeatureVectorizer:
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

            # Auto-infer root category keywords if sub-keywords match
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

            # Universal Hash Signatures
            for tok in tokens:
                h = int(hashlib.md5(tok.encode("utf-8")).hexdigest()[:8], 16)
                idx = h % self.dim
                sign = 1.0 if (h & 1) else -1.0
                vec[idx] += sign * 1.0

            norm = np.linalg.norm(vec)
            if norm > 1e-6:
                vec = vec / norm
            else:
                vec = np.ones(self.dim, dtype=np.float32) / np.sqrt(self.dim)

            results.append(vec)

        return results[0] if is_single else np.array(results)

def cosine_sim(v1, v2):
    return float(np.dot(v1, v2))

vec = SemanticFeatureVectorizer()
q_mobile = vec.encode("mobile")
iphone = vec.encode("Product: Apple iPhone 15 Pro Max | Category: Smartphones & Tablets | Brand: Apple | Tags: apple, iphone, smartphone, 5g, mobile")
samsung = vec.encode("Product: Samsung Galaxy S24 Ultra | Category: Smartphones & Tablets | Brand: Samsung | Tags: samsung, galaxy, android, smartphone, phone")
sony_audio = vec.encode("Product: Sony WH-1000XM5 Wireless Headphones | Category: Audio & Headphones | Brand: Sony | Tags: sony, headphones, audio, anc")
macbook = vec.encode("Product: Apple MacBook Pro 16 | Category: Laptops & Computers | Brand: Apple | Tags: apple, macbook, laptop, m3")
burberry = vec.encode("Product: Burberry The Pimlico Heritage Car Coat | Category: Jackets & Outerwear | Brand: Burberry | Tags: burberry, coat, trench")

print("cosine(mobile, iPhone):", round(cosine_sim(q_mobile, iphone), 4))
print("cosine(iPhone, Samsung):", round(cosine_sim(iphone, samsung), 4))
print("cosine(iPhone, MacBook):", round(cosine_sim(iphone, macbook), 4))
print("cosine(iPhone, Sony Audio):", round(cosine_sim(iphone, sony_audio), 4))
print("cosine(iPhone, Burberry Coat):", round(cosine_sim(iphone, burberry), 4))
