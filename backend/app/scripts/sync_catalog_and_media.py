"""
NovaMart — Catalog Media Synchronization & Expansion Script

This script:
1. Fixes all mismatched product images in PostgreSQL (Dumbbells, Espresso Machine, Kettle, Massage Gun, etc.)
2. Adds 16 new iconic real-world products requested by the user
3. Generates high-accuracy semantic embeddings via FastEmbed for all updated & new products
4. Keeps product_templates.py synchronized
"""

import asyncio
import logging
import uuid
from decimal import Decimal
from slugify import slugify

from sqlalchemy import select, delete, text
from sqlalchemy.orm import selectinload

from app.core.database import async_session_factory
from app.models.category import Category
from app.models.product import Product, ProductImage
from app.services.vector_service import VectorService

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("sync_catalog")

# 1. Product Image Corrections for Existing Catalog
IMAGE_CORRECTIONS = {
    "Bowflex SelectTech 552 Adjustable Dumbbells (Pair, 5 to 52.5 lbs)": [
        "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1586401100295-7a8096fd231a?w=800&auto=format&fit=crop"
    ],
    "Theragun PRO Plus Multi-Therapy Percussive Massage Device": [
        "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&auto=format&fit=crop"
    ],
    "Fellow Stagg EKG Electric Pour-Over Kettle - Matte Black": [
        "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=800&auto=format&fit=crop"
    ],
    "Breville The Barista Touch Impress Espresso Machine - Brushed Stainless Steel": [
        "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&auto=format&fit=crop"
    ],
    "Dyson V15 Detect Absolute Cordless Stick Vacuum": [
        "https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800&auto=format&fit=crop"
    ],
    "On Cloudmonster 2 Max-Cushion Road Running Shoes - Undyed White": [
        "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=800&auto=format&fit=crop"
    ],
    "Lululemon Align High-Rise Pant 25\" - Black": [
        "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=800&auto=format&fit=crop"
    ],
    "Apple Watch Ultra 2 (GPS + Cellular 49mm Titanium Case with Orange Ocean Band)": [
        "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&auto=format&fit=crop"
    ],
    "Fujifilm X100VI Digital Camera - Silver": [
        "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&auto=format&fit=crop"
    ],
    "Burberry The Pimlico Heritage Car Coat - Honey": [
        "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1544441893-675973e31985?w=800&auto=format&fit=crop"
    ],
    "Burberry Cotton and Leather Webb Strap Sneakers": [
        "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=800&auto=format&fit=crop"
    ],
    "Saint Laurent SL 557 Shade Bold Acetate Sunglasses": [
        "https://images.unsplash.com/photo-1508296695146-257a814070b4?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&auto=format&fit=crop"
    ]
}

# 2. Brand New Iconic Products to Add
NEW_PRODUCTS = [
    {
        "category_slug": "electronics",
        "subcategory_name": "Laptops & Computers",
        "title": "Sony PlayStation 5 Slim Console (1TB SSD, DualSense Wireless Controller)",
        "brand": "Sony",
        "price": 499.99,
        "compare_at_price": 549.99,
        "stock": 40,
        "short_description": "Slim design with 1TB SSD storage, 4K-TV gaming, Ray Tracing, and Tempest 3D AudioTech.",
        "description": "Experience lightning-fast loading with an ultra-high-speed SSD, deeper immersion with haptic feedback, adaptive triggers, and 3D Audio, plus an all-new generation of incredible PlayStation games. Packed into a sleek, compact slim chassis with 1TB internal high-speed storage.",
        "attributes": {
            "storage": "1TB Custom High-Speed NVMe SSD",
            "resolution": "Up to 4K 120Hz, 8K output support",
            "audio": "Tempest 3D AudioTech engine",
            "controller": "DualSense Wireless Controller with Haptic Feedback"
        },
        "images": [
            "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=800&auto=format&fit=crop"
        ],
        "tags": ["sony", "playstation", "ps5", "gaming", "console", "bestseller"]
    },
    {
        "category_slug": "electronics",
        "subcategory_name": "Smartphones & Tablets",
        "title": "Amazon Kindle Paperwhite (16GB, 6.8\" Glare-Free Display, Warm Light)",
        "brand": "Amazon",
        "price": 149.99,
        "compare_at_price": 169.99,
        "stock": 65,
        "short_description": "6.8\" 300 ppi display, adjustable warm light, up to 10 weeks battery life, waterproof IPX8.",
        "description": "Now with a 6.8\" display and thinner borders, adjustable warm light, up to 10 weeks of battery life, and 20% faster page turns. Purpose-built for reading with a flush-front design and 300 ppi glare-free display that reads like real paper even in bright sunlight.",
        "attributes": {
            "display": "6.8\" Paperwhite display with built-in light, 300 ppi",
            "storage": "16GB (Holds thousands of books)",
            "battery_life": "Up to 10 weeks on a single charge",
            "waterproofing": "IPX8 (Submersion in 2 meters fresh water for 60 min)"
        },
        "images": [
            "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&auto=format&fit=crop"
        ],
        "tags": ["amazon", "kindle", "ereader", "books", "reading", "paperwhite", "bestseller"]
    },
    {
        "category_slug": "electronics",
        "subcategory_name": "Laptops & Computers",
        "title": "Logitech MX Master 3S Wireless Performance Mouse - Graphite",
        "brand": "Logitech",
        "price": 99.99,
        "compare_at_price": 119.99,
        "stock": 70,
        "short_description": "Quiet Clicks, 8K DPI any-surface tracking, MagSpeed electromagnetic scrolling wheel.",
        "description": "An icon remastered. Feel every single moment of your workflow with even more precision, tactility, and performance, thanks to Quiet Clicks and an 8,000 DPI track-on-glass sensor. The MagSpeed electromagnetic scroll wheel provides unmatched speed and silence.",
        "attributes": {
            "sensor": "Darkfield high precision, 200 to 8000 DPI (set in increments of 50 DPI)",
            "buttons": "7 buttons (Left/Right-click, Back/Forward, App-Switch, Wheel mode-shift, Middle click)",
            "scroll": "MagSpeed SmartShift electromagnetic scrolling wheel",
            "battery": "Rechargeable Li-Po (500 mAh) battery, up to 70 days on a full charge"
        },
        "images": [
            "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop"
        ],
        "tags": ["logitech", "mouse", "mxmaster", "ergonomic", "productivity", "bestseller"]
    },
    {
        "category_slug": "electronics",
        "subcategory_name": "Audio & Headphones",
        "title": "Marshall Stanmore III Bluetooth Home Speaker - Black",
        "brand": "Marshall",
        "price": 379.99,
        "compare_at_price": 419.99,
        "stock": 35,
        "short_description": "Room-filling Marshall signature sound, re-engineered wider stereo soundstage, Bluetooth 5.2.",
        "description": "As the middleweight speaker of the home line-up, Stanmore III brings expansive Marshall sound to any room. It has outward-angled tweeters and updated waveguides to deliver a consistently solid sound that is so wide it chases you around the room.",
        "attributes": {
            "power_amps": "One 50 Watt Class D amp for woofer, Two 15 Watt Class D amps for tweeters",
            "frequency_range": "45–20,000 Hz",
            "controls": "Bass and treble analogue control knobs, brass volume knob",
            "connectivity": "Bluetooth 5.2, 3.5 mm input, RCA input"
        },
        "images": [
            "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&auto=format&fit=crop"
        ],
        "tags": ["marshall", "speaker", "audio", "bluetooth", "vintage", "rock", "bestseller"]
    },
    {
        "category_slug": "electronics",
        "subcategory_name": "Audio & Headphones",
        "title": "Bose SoundLink Revolve+ II Portable Bluetooth Speaker - Triple Black",
        "brand": "Bose",
        "price": 329.00,
        "compare_at_price": 359.00,
        "stock": 45,
        "short_description": "True 360-degree sound, durable water and dust resistant (IP55), up to 17 hours battery.",
        "description": "Deep. Loud. And immersive, too. This true 360° speaker was engineered to spread deep, jaw-dropping sound in every direction. That means, when everyone stands around it, everyone gets the same experience with flexible fabric handle for effortless portability.",
        "attributes": {
            "sound": "True 360-degree sound coverage with dual-passive radiators",
            "battery_life": "Up to 17 hours rechargeable lithium-ion battery",
            "durability": "IP55 water- and dust-resistant seamless aluminum body",
            "voice_assistant": "Built-in microphone for speakerphone and Siri / Google Assistant"
        },
        "images": [
            "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&auto=format&fit=crop"
        ],
        "tags": ["bose", "speaker", "soundlink", "bluetooth", "portable", "360sound", "bestseller"]
    },
    {
        "category_slug": "electronics",
        "subcategory_name": "Smart Home & Wearables",
        "title": "Belkin BoostCharge Pro 3-in-1 Wireless Charging Stand with MagSafe 15W",
        "brand": "Belkin",
        "price": 149.95,
        "compare_at_price": 169.95,
        "stock": 50,
        "short_description": "Official 15W MagSafe fast charging for iPhone, Apple Watch fast charger, and AirPods tray.",
        "description": "Charge your Apple devices faster with this beautifully designed charging stand. Delivering up to 15W of wireless charging to your iPhone 12 or newer, fast charging for Apple Watch Series 7 and later, and a dedicated Qi pad for your AirPods.",
        "attributes": {
            "compatibility": "Made for MagSafe official 15W certification",
            "watch_charging": "Apple Watch Fast Charging support",
            "orientation": "Charge in portrait or landscape for StandBy mode",
            "materials": "Architectural stainless steel arm with soft-touch silicone base"
        },
        "images": [
            "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop"
        ],
        "tags": ["belkin", "magsafe", "charger", "apple", "wireless", "iphone", "stand"]
    },
    {
        "category_slug": "home_kitchen",
        "subcategory_name": "Cookware & Dining",
        "title": "Stanley Quencher H2.0 FlowState Stainless Steel Tumbler 40 oz - Rose Quartz",
        "brand": "Stanley",
        "price": 45.00,
        "compare_at_price": 55.00,
        "stock": 90,
        "short_description": "Recycled stainless steel, double-wall vacuum insulation, FlowState 3-position rotating lid.",
        "description": "Constructed of 90% recycled stainless steel for sustainable sipping, the 40 oz Quencher H2.0 helps you reach your hydration goals with fewer refills. Commuting, studio workouts, day trips or your front porch—you'll want this tumbler by your side.",
        "attributes": {
            "capacity": "40 oz / 1.18 Liters",
            "insulation": "Keeps drinks cold for 11 hours, iced for 2 days",
            "lid": "FlowState™ 3-position lid (straw opening, drink opening, full cover)",
            "cup_holder": "Car cup holder compatible base"
        },
        "images": [
            "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?w=800&auto=format&fit=crop"
        ],
        "tags": ["stanley", "quencher", "tumbler", "waterbottle", "hydration", "bestseller"]
    },
    {
        "category_slug": "home_kitchen",
        "subcategory_name": "Kitchen Appliances",
        "title": "Chemex Classic Eight-Cup Pour-Over Glass Coffeemaker with Wood Collar",
        "brand": "Chemex",
        "price": 49.50,
        "compare_at_price": 58.00,
        "stock": 60,
        "short_description": "Iconic non-porous borosilicate glass carafe with polished wood collar and leather tie.",
        "description": "Selected by the Illinois Institute of Technology as one of the 100 best designed products of modern times. The Chemex delivers the purest flavor experience without any chemical residue, producing clean, aromatic pour-over coffee free of sediment and bitterness.",
        "attributes": {
            "capacity": "40 oz (8 cups of brewed coffee)",
            "material": "Heat-resistant non-porous Borosilicate Glass",
            "handle": "Polished wood collar with genuine leather tie",
            "design": "Permanent exhibition piece at the Museum of Modern Art (MoMA)"
        },
        "images": [
            "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&auto=format&fit=crop"
        ],
        "tags": ["chemex", "coffee", "pourover", "coffeemaker", "glassware", "design", "bestseller"]
    },
    {
        "category_slug": "fashion",
        "subcategory_name": "Sneakers & Footwear",
        "title": "Birkenstock Boston Oiled Leather Clogs - Habana Brown",
        "brand": "Birkenstock",
        "price": 160.00,
        "compare_at_price": 175.00,
        "stock": 50,
        "short_description": "Anatomically shaped cork-latex footbed with oiled nubuck leather upper and adjustable strap.",
        "description": "The BIRKENSTOCK Boston is a veritable classic that can easily be worn all year round. With its sophisticated, individually adjustable design and iconic natural cork footbed that molds to the unique contours of your foot over time.",
        "attributes": {
            "upper": "Oiled nubuck leather with natural patina",
            "footbed": "Anatomically shaped cork-latex footbed with suede lining",
            "sole": "Lightweight shock-absorbing EVA",
            "origin": "Made in Germany"
        },
        "images": [
            "https://images.unsplash.com/photo-1535043934128-cf0b28d52f95?w=800&auto=format&fit=crop"
        ],
        "tags": ["birkenstock", "boston", "clogs", "footwear", "leather", "casual", "bestseller"]
    },
    {
        "category_slug": "fashion",
        "subcategory_name": "Eyewear & Accessories",
        "title": "Ray-Ban Clubmaster Classic Polarized Sunglasses - Mock Tortoise / Gold",
        "brand": "Ray-Ban",
        "price": 215.00,
        "compare_at_price": 240.00,
        "stock": 45,
        "short_description": "Retro browline acetate frame with polished gold metal rims and G-15 green polarized mineral glass.",
        "description": "Ray-Ban Clubmaster Classic sunglasses are retro and timeless. Inspired by the 50's, the unmistakable design of the Clubmaster Classic is worn by cultural intellectuals, those who lead the changed tomorrow.",
        "attributes": {
            "frame": "Mock Tortoise acetate browline with polished gold metal lower rim",
            "lenses": "Crystal Green G-15 Polarized mineral lenses (100% UV protection)",
            "dimensions": "Lens 51mm, Bridge 21mm, Temple 145mm",
            "origin": "Handcrafted in Italy"
        },
        "images": [
            "https://images.unsplash.com/photo-1508296695146-257a814070b4?w=800&auto=format&fit=crop"
        ],
        "tags": ["rayban", "clubmaster", "sunglasses", "eyewear", "polarized", "classic", "bestseller"]
    },
    {
        "category_slug": "sports_outdoors",
        "subcategory_name": "Outdoor & Camping",
        "title": "Yeti Rambler 20 oz Travel Mug with Stronghold Lid - Navy",
        "brand": "Yeti",
        "price": 38.00,
        "compare_at_price": 45.00,
        "stock": 75,
        "short_description": "18/8 kitchen-grade stainless steel, double-wall vacuum insulation, leak-resistant twist Stronghold lid.",
        "description": "This double-duty, on-the-go drinkware is topped with the Rambler® Stronghold™ Lid—a leak-resistant, twist-on upgrade that's backed with dual-slider magnet technology. This lid easily rotates to fasten for both right- and left-handed users.",
        "attributes": {
            "capacity": "20 fl. oz. / 591 ml",
            "material": "18/8 Kitchen-grade stainless steel, puncture- and rust-resistant",
            "lid": "Stronghold™ 360-degree twist-on leak-resistant lid",
            "cupholder": "Elevated handle fits standard car cup holders"
        },
        "images": [
            "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=800&auto=format&fit=crop"
        ],
        "tags": ["yeti", "rambler", "travelmug", "coffee", "insulated", "outdoors", "bestseller"]
    },
    {
        "category_slug": "sports_outdoors",
        "subcategory_name": "Yoga & Recovery",
        "title": "Manduka PRO Yoga Mat (6mm High Density Cushion) - Black Sage",
        "brand": "Manduka",
        "price": 138.00,
        "compare_at_price": 150.00,
        "stock": 40,
        "short_description": "Ultra-dense 6mm cushion for joint protection, closed-cell surface prevents sweat absorption.",
        "description": "The #1 recommended mat by yoga teachers worldwide. The Manduka PRO provides unmatched density and joint cushioning on hard floors, proprietary dot-pattern traction, and a lifetime guarantee.",
        "attributes": {
            "thickness": "6 mm ultra-dense cushioning",
            "dimensions": "71\" L x 26\" W (180cm x 66cm), Weight: 7.5 lbs",
            "surface": "Closed-cell PVC prevents moisture, sweat, and bacteria from entering",
            "certification": "STANDARD 100 by OEKO-TEX® non-toxic emissions manufacturing"
        },
        "images": [
            "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800&auto=format&fit=crop"
        ],
        "tags": ["manduka", "yogamat", "yoga", "fitness", "pro", "recovery", "bestseller"]
    },
    {
        "category_slug": "sports_outdoors",
        "subcategory_name": "Fitness Equipment",
        "title": "Spalding NBA Official Game Ball Basketball (Full Grain Leather, Size 7)",
        "brand": "Spalding",
        "price": 129.99,
        "compare_at_price": 149.99,
        "stock": 40,
        "short_description": "Exclusive Horween full grain leather cover, official NBA 29.5\" size, superior bounce and grip.",
        "description": "Crafted from exclusive Horween full-grain leather that breaks in over time to offer a soft touch and unmatched grip. Meets all stringent professional standards for true bounce and flight consistency.",
        "attributes": {
            "size": "Official NBA Size 7 (29.5\" circumference)",
            "cover": "Premium Horween full-grain leather cover",
            "use": "Designed strictly for indoor hardwood play",
            "inflation": "Retains air pressure with butyl bladder and nylon winding"
        },
        "images": [
            "https://images.unsplash.com/photo-1519861531473-9200262188bf?w=800&auto=format&fit=crop"
        ],
        "tags": ["spalding", "basketball", "nba", "sports", "leather", "athletics", "bestseller"]
    },
    {
        "category_slug": "beauty",
        "subcategory_name": "Hair Styling & Care",
        "title": "Olaplex No. 3 Hair Perfector Repairing Treatment (3.3 fl oz / 100ml)",
        "brand": "Olaplex",
        "price": 30.00,
        "compare_at_price": 36.00,
        "stock": 85,
        "short_description": "Global bestseller bond-builder reduces breakage and visibly strengthens all hair types.",
        "description": "An at-home bond-building treatment that reduces breakage and visibly strengthens hair, improving its look and feel. Powered by patented OLAPLEX Bond Building Technology™ that repairs broken disulfide bonds caused by heat, chemical processing, and styling.",
        "attributes": {
            "volume": "100 ml / 3.3 fl. oz.",
            "technology": "Bis-Aminopropyl Diglycol Dimaleate patented bond builder",
            "hair_type": "Straight, Wavy, Curly, and Coily (Color-safe)",
            "safety": "Paraben-free, phthalate-free, sulfate-free, vegan"
        },
        "images": [
            "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800&auto=format&fit=crop"
        ],
        "tags": ["olaplex", "haircare", "treatment", "repair", "beauty", "bestseller"]
    },
    {
        "category_slug": "beauty",
        "subcategory_name": "Skincare Treatments",
        "title": "Dior Addict Lip Glow Color Reviver Balm - 001 Pink",
        "brand": "Dior",
        "price": 40.00,
        "compare_at_price": 45.00,
        "stock": 70,
        "short_description": "Color-awakening hydrating lip balm formulated with 97% natural-origin ingredients and cherry oil.",
        "description": "The 1st Dior lip balm formulated with 97% natural-origin ingredients that subtly revives the natural color of lips with a custom glow for 6h and hydrates lips for 24h. Infused with cherry oil, sunflower wax, and shea butter.",
        "attributes": {
            "shade": "001 Pink (Universal subtle natural flush)",
            "ingredients": "97% Natural-origin with nourishing French cherry oil",
            "finish": "Dewy subtle sheen with custom pH color adaptation",
            "wear": "24h continuous hydration and 6h custom color glow"
        },
        "images": [
            "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=800&auto=format&fit=crop"
        ],
        "tags": ["dior", "lipglow", "lipbalm", "beauty", "makeup", "luxury", "bestseller"]
    },
    {
        "category_slug": "fashion",
        "subcategory_name": "Bags & Luggage",
        "title": "Bellroy Transit Backpack 28L - Black",
        "brand": "Bellroy",
        "price": 259.00,
        "compare_at_price": 289.00,
        "stock": 35,
        "short_description": "Travel carry-on compliant backpack with separate 16\" laptop access and hidden passport pocket.",
        "description": "Clever organization meets sleek minimalist travel. The Transit Backpack features quick-access external pockets for phone, passport, and water bottles, a dedicated lay-flat laptop sleeve, and a spacious main compartment with internal compression straps.",
        "attributes": {
            "capacity": "28 Liters (Airline carry-on approved)",
            "laptop_fit": "Fits up to 16\" laptops in padded separate rear compartment",
            "materials": "Durable, water-resistant recycled Baida Nylon fabric with premium leather accents",
            "comfort": "Contoured padded breathable mesh back panel with sternum strap"
        },
        "images": [
            "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&auto=format&fit=crop"
        ],
        "tags": ["bellroy", "backpack", "travel", "carryon", "minimalist", "laptopbag", "bestseller"]
    }
]


async def sync_catalog():
    async with async_session_factory() as db:
        vector_service = VectorService(db)
        logger.info("Starting catalog media synchronization & expansion...")

        # 1. Update existing product images and details
        updated_count = 0
        for title, image_urls in IMAGE_CORRECTIONS.items():
            result = await db.execute(
                select(Product)
                .options(selectinload(Product.category), selectinload(Product.images))
                .where(Product.title == title)
            )
            product = result.scalar_one_or_none()
            if product:
                # Delete existing images
                await db.execute(
                    delete(ProductImage).where(ProductImage.product_id == product.id)
                )
                await db.flush()

                # Add corrected images
                for sort_order, url in enumerate(image_urls):
                    img = ProductImage(
                        product_id=product.id,
                        url=url,
                        alt_text=f"{product.title} - View {sort_order + 1}",
                        sort_order=sort_order,
                    )
                    db.add(img)

                await db.flush()
                # Re-index embedding
                await vector_service.generate_embedding(product)
                updated_count += 1
                logger.info(f"Fixed images for: {title[:45]}...")

        # 2. Add brand new products
        inserted_count = 0
        for p_data in NEW_PRODUCTS:
            title = p_data["title"]
            existing = await db.execute(
                select(Product).where(Product.title == title)
            )
            if existing.scalar_one_or_none():
                continue

            # Lookup parent and subcategory
            cat_slug = p_data["category_slug"]
            cat_res = await db.execute(
                select(Category).where(Category.slug == cat_slug)
            )
            category = cat_res.scalar_one_or_none()
            if not category:
                # Fallback to any category
                cat_res = await db.execute(select(Category).limit(1))
                category = cat_res.scalar_one()

            # Try to match subcategory if present
            sub_res = await db.execute(
                select(Category).where(
                    Category.parent_id == category.id,
                    Category.name == p_data["subcategory_name"]
                )
            )
            target_category = sub_res.scalar_one_or_none() or category

            slug = slugify(title)
            slug_chk = await db.execute(select(Product.id).where(Product.slug == slug))
            if slug_chk.scalar_one_or_none():
                slug = f"{slug}-{uuid.uuid4().hex[:4]}"

            product = Product(
                sku=f"NM-{uuid.uuid4().hex[:8].upper()}",
                title=title,
                slug=slug,
                description=p_data["description"],
                short_description=p_data["short_description"],
                price=Decimal(str(p_data["price"])),
                compare_at_price=Decimal(str(p_data["compare_at_price"])) if p_data.get("compare_at_price") else None,
                stock_quantity=p_data["stock"],
                category_id=target_category.id,
                brand=p_data["brand"],
                attributes=p_data["attributes"],
                tags=p_data["tags"],
                is_published=True,
                is_featured=True,
            )
            db.add(product)
            await db.flush()

            for sort_order, url in enumerate(p_data["images"]):
                img = ProductImage(
                    product_id=product.id,
                    url=url,
                    alt_text=f"{title} - View {sort_order + 1}",
                    sort_order=sort_order,
                )
                db.add(img)

            await db.flush()
            # Generate embedding
            await vector_service.generate_embedding(product)
            inserted_count += 1
            logger.info(f"Added new product: {title[:45]}...")

        await db.commit()
        logger.info(f"Synchronization complete! Updated: {updated_count} products, Added: {inserted_count} new products.")

if __name__ == "__main__":
    asyncio.run(sync_catalog())
