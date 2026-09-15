"""
NovaMart — Authentic E-Commerce Product Catalog

Curated collection of real-world recognizable products across major categories
with accurate specifications, pricing, brand identities, and high-resolution imagery.
"""

ORIGINAL_CATEGORIES = {
    "electronics": {
        "name": "Electronics",
        "icon": "⚡",
        "description": "Premium consumer electronics, computing, mobile, and audio",
        "subcategories": ["Laptops & Computers", "Smartphones & Tablets", "Audio & Headphones", "Cameras & Optics", "Smart Home & Wearables"]
    },
    "fashion": {
        "name": "Fashion & Apparel",
        "icon": "👕",
        "description": "Iconic footwear, designer denim, outerwear, and accessories",
        "subcategories": ["Sneakers & Footwear", "Jackets & Outerwear", "Jeans & Trousers", "Eyewear & Accessories", "Bags & Luggage"]
    },
    "home_kitchen": {
        "name": "Home & Kitchen",
        "icon": "🏡",
        "description": "Modern kitchenware, smart appliances, ergonomic living, and cookware",
        "subcategories": ["Kitchen Appliances", "Cookware & Dining", "Cleaning & Vacuums", "Ergonomic Furniture", "Smart Lighting"]
    },
    "beauty": {
        "name": "Beauty & Personal Care",
        "icon": "✨",
        "description": "Luxury skincare, hair care, fragrances, and personal grooming",
        "subcategories": ["Hair Styling & Care", "Skincare Treatments", "Fragrances & Perfumes", "Oral Care & Wellness"]
    },
    "sports_outdoors": {
        "name": "Sports & Outdoors",
        "icon": "🏔️",
        "description": "High-performance fitness equipment, outdoor gear, and athletic tech",
        "subcategories": ["Fitness Equipment", "Yoga & Recovery", "GPS & Sports Watches", "Outdoor & Camping"]
    }
}

AUTHENTIC_PRODUCTS = [
    # ─── ELECTRONICS: Laptops & Computers ───────────────────
    {
        "category": "electronics",
        "subcategory": "Laptops & Computers",
        "title": "Apple MacBook Pro 16\" (M3 Max, 36GB Unified Memory, 1TB SSD) - Space Black",
        "brand": "Apple",
        "price": 3499.00,
        "compare_at_price": 3799.00,
        "stock": 45,
        "short_description": "Liquid Retina XDR display, M3 Max chip with 16-core CPU, up to 22 hours of battery life.",
        "description": "The 16-inch MacBook Pro blasts forward with M3 Max, an extraordinarily advanced chip that brings massive performance and capabilities for the most extreme workflows. Built with 3-nanometer technology and featuring an all-new GPU architecture, it's the most advanced chip ever built for a personal computer. With industry-leading battery life — up to 22 hours — and a breathtaking Liquid Retina XDR display, it's a pro laptop without equal.",
        "attributes": {
            "processor": "Apple M3 Max (16-core CPU, 40-core GPU)",
            "ram": "36GB Unified Memory",
            "storage": "1TB Superfast NVMe SSD",
            "display": "16.2-inch Liquid Retina XDR (3456x2234, 120Hz ProMotion)",
            "battery_life": "Up to 22 hours",
            "ports": "3x Thunderbolt 4, HDMI, SDXC card slot, MagSafe 3",
            "weight": "2.16 kg (4.8 lbs)"
        },
        "images": [
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800&auto=format&fit=crop"
        ],
        "tags": ["apple", "macbook", "laptop", "m3", "pro", "bestseller", "premium"]
    },
    {
        "category": "electronics",
        "subcategory": "Laptops & Computers",
        "title": "Dell XPS 15 9530 (13th Gen Intel Core i9-13900H, 32GB RAM, 1TB SSD, RTX 4070)",
        "brand": "Dell",
        "price": 2399.00,
        "compare_at_price": 2699.00,
        "stock": 30,
        "short_description": "3.5K OLED InfinityEdge touch display, NVIDIA GeForce RTX 4070 8GB GDDR6, CNC machined aluminum.",
        "description": "Immerse yourself in content with stunning 3.5K OLED InfinityEdge display that delivers vivid color and sharp contrast. Powered by 13th Gen Intel Core i9 processor and GeForce RTX 4070 graphics, the XPS 15 provides creator-level power in a breathtaking 18mm thin chassis made from precision CNC machined aluminum with carbon fiber palm rest.",
        "attributes": {
            "processor": "Intel Core i9-13900H (14-core, up to 5.4 GHz)",
            "ram": "32GB DDR5 4800MHz",
            "storage": "1TB M.2 PCIe NVMe SSD",
            "graphics": "NVIDIA GeForce RTX 4070 8GB GDDR6",
            "display": "15.6\" 3.5K (3456x2160) OLED Touch 400-nit",
            "weight": "1.92 kg (4.23 lbs)"
        },
        "images": [
            "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop"
        ],
        "tags": ["dell", "xps", "laptop", "windows", "creator", "oled", "bestseller"]
    },
    {
        "category": "electronics",
        "subcategory": "Laptops & Computers",
        "title": "ASUS ROG Zephyrus G14 Gaming Laptop (AMD Ryzen 9 8945HS, RTX 4070, 32GB RAM, 1TB SSD)",
        "brand": "ASUS",
        "price": 1999.99,
        "compare_at_price": 2199.99,
        "stock": 25,
        "short_description": "14\" 3K 120Hz ROG Nebula OLED display, ultra-portable 1.5kg chassis with CNC slash lighting.",
        "description": "Game and create anywhere with the ROG Zephyrus G14. Featuring an all-aluminum CNC machined unibody design with customizable Slash Lighting on the lid, this thin-and-light powerhouse is packed with an AMD Ryzen 9 8945HS processor and NVIDIA GeForce RTX 4070 Laptop GPU, cooled by ROG Intelligent Cooling with liquid metal.",
        "attributes": {
            "processor": "AMD Ryzen 9 8945HS with Ryzen AI (up to 5.2 GHz)",
            "ram": "32GB LPDDR5X 6400MHz",
            "storage": "1TB PCIe 4.0 NVMe M.2 SSD",
            "graphics": "NVIDIA GeForce RTX 4070 8GB GDDR6",
            "display": "14\" 3K (2880 x 1800) OLED 120Hz 0.2ms G-SYNC",
            "weight": "1.5 kg (3.31 lbs)"
        },
        "images": [
            "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&auto=format&fit=crop"
        ],
        "tags": ["asus", "rog", "gaming", "laptop", "oled", "ryzen", "rtx"]
    },

    # ─── ELECTRONICS: Smartphones & Tablets ────────────────
    {
        "category": "electronics",
        "subcategory": "Smartphones & Tablets",
        "title": "Apple iPhone 15 Pro Max (256GB, Natural Titanium)",
        "brand": "Apple",
        "price": 1199.00,
        "compare_at_price": 1299.00,
        "stock": 65,
        "short_description": "Forged in titanium, A17 Pro chip, customizable Action button, 5x Telephoto camera.",
        "description": "iPhone 15 Pro Max features a strong and light aerospace-grade titanium design with textured matte-glass back. It also features a Ceramic Shield front that's tougher than any smartphone glass. A17 Pro chip brings a monster win for gaming with hardware-accelerated ray tracing. The 48MP Main camera is more advanced than ever, capturing super-high-resolution photos with a new level of detail and color, plus 5x optical zoom.",
        "attributes": {
            "display": "6.7\" Super Retina XDR OLED (120Hz ProMotion, 2000 nits)",
            "processor": "A17 Pro (6-core CPU, 6-core GPU, Neural Engine)",
            "storage": "256GB NVMe",
            "camera": "48MP Main + 12MP Ultra Wide + 12MP 5x Telephoto",
            "chassis": "Grade 5 Titanium with Ceramic Shield front",
            "connectivity": "5G, Wi-Fi 6E, Bluetooth 5.3, USB-C 10Gbps"
        },
        "images": [
            "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=800&auto=format&fit=crop"
        ],
        "tags": ["apple", "iphone", "smartphone", "5g", "titanium", "camera", "bestseller"]
    },
    {
        "category": "electronics",
        "subcategory": "Smartphones & Tablets",
        "title": "Samsung Galaxy S24 Ultra 5G (512GB, Titanium Gray) with Galaxy AI & S-Pen",
        "brand": "Samsung",
        "price": 1299.99,
        "compare_at_price": 1419.99,
        "stock": 50,
        "short_description": "Galaxy AI, 200MP camera system, Snapdragon 8 Gen 3 for Galaxy, built-in S Pen.",
        "description": "Meet Galaxy S24 Ultra, the ultimate form of Galaxy Ultra with a new titanium exterior and a 6.8-inch flat display. Unleash whole new levels of creativity, productivity, and possibility starting with the most important device in your life — your phone. Search like never before with Circle to Search, get real-time voice translation on a call, and format your notes into a clear summary.",
        "attributes": {
            "display": "6.8\" Dynamic LTPO AMOLED 2X (1-120Hz, 2600 nits)",
            "processor": "Snapdragon 8 Gen 3 for Galaxy",
            "ram": "12GB RAM",
            "storage": "512GB UFS 4.0",
            "camera": "200MP Wide + 50MP 5x Periscope + 10MP 3x Telephoto + 12MP Ultra-wide",
            "battery": "5000mAh with 45W wired charging"
        },
        "images": [
            "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800&auto=format&fit=crop"
        ],
        "tags": ["samsung", "galaxy", "s24", "android", "ai", "spen", "bestseller"]
    },
    {
        "category": "electronics",
        "subcategory": "Smartphones & Tablets",
        "title": "Apple iPad Pro 12.9\" (M2, Wi-Fi, 256GB) - Space Gray",
        "brand": "Apple",
        "price": 1099.00,
        "compare_at_price": 1199.00,
        "stock": 40,
        "short_description": "Liquid Retina XDR display with Mini-LED backlighting, M2 chip, Apple Pencil hover.",
        "description": "iPad Pro. With mind-blowing performance from the M2 chip, superfast wireless connectivity, and next-generation Apple Pencil experience. Plus powerful productivity features in iPadOS. It's the ultimate iPad experience.",
        "attributes": {
            "processor": "Apple M2 Chip (8-core CPU, 10-core GPU)",
            "display": "12.9\" Liquid Retina XDR Mini-LED (2732x2048, 1000 nits)",
            "storage": "256GB",
            "cameras": "12MP Wide and 10MP Ultra Wide back cameras, LiDAR Scanner",
            "audio": "Four speaker audio and five studio-quality microphones"
        },
        "images": [
            "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&auto=format&fit=crop"
        ],
        "tags": ["apple", "ipad", "tablet", "m2", "retina", "drawing"]
    },

    # ─── ELECTRONICS: Audio & Headphones ────────────────────
    {
        "category": "electronics",
        "subcategory": "Audio & Headphones",
        "title": "Sony WH-1000XM5 Wireless Industry Leading Noise Canceling Headphones - Black",
        "brand": "Sony",
        "price": 398.00,
        "compare_at_price": 449.00,
        "stock": 80,
        "short_description": "Auto NC Optimizer with 8 microphones, up to 30 hours battery, ultra-comfortable lightweight design.",
        "description": "The WH-1000XM5 headphones rewrite the rules for distraction-free listening. Two processors control 8 microphones for unprecedented noise cancellation and exceptional call quality. With a newly developed driver, DSEE - Extreme and Hi-Res audio support, these headphones provide awe-inspiring audio quality without compromise.",
        "attributes": {
            "anc": "Industry-leading Active Noise Cancellation with V1 & QN1 processors",
            "battery_life": "Up to 30 hours (ANC on), 40 hours (ANC off)",
            "quick_charge": "3 minutes gives 3 hours playback",
            "microphones": "8 microphones with AI beamforming",
            "codecs": "LDAC, AAC, SBC",
            "weight": "250 grams"
        },
        "images": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800&auto=format&fit=crop"
        ],
        "tags": ["sony", "headphones", "anc", "wireless", "audiophile", "bestseller"]
    },
    {
        "category": "electronics",
        "subcategory": "Audio & Headphones",
        "title": "Apple AirPods Pro (2nd Generation) with MagSafe Case (USB-C)",
        "brand": "Apple",
        "price": 249.00,
        "compare_at_price": 279.00,
        "stock": 110,
        "short_description": "Up to 2x more Active Noise Cancellation, Adaptive Audio, Transparency mode, Personalized Spatial Audio.",
        "description": "AirPods Pro (2nd generation) with USB-C deliver up to 2x more Active Noise Cancellation than the previous generation, with Transparency mode that enables you to hear the world around you, and all-new Adaptive Audio that dynamically tailors noise control to your environment.",
        "attributes": {
            "chip": "Apple H2 headphone chip, Apple U1 chip in case",
            "battery_life": "Up to 6 hours (single charge), up to 30 hours with case",
            "charging": "USB-C, MagSafe, Apple Watch charger, Qi-certified",
            "water_resistance": "IP54 dust, sweat, and water resistant",
            "features": "Personalized Spatial Audio with dynamic head tracking"
        },
        "images": [
            "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800&auto=format&fit=crop"
        ],
        "tags": ["apple", "airpods", "earbuds", "anc", "wireless", "bestseller"]
    },
    {
        "category": "electronics",
        "subcategory": "Audio & Headphones",
        "title": "Bose QuietComfort Ultra Wireless Noise Cancelling Headphones - White Smoke",
        "brand": "Bose",
        "price": 429.00,
        "compare_at_price": 479.00,
        "stock": 55,
        "short_description": "World-class noise cancellation, groundbreaking spatialized audio, custom tune technology.",
        "description": "High-fidelity audio and legendary noise cancellation come together with Bose Immersive Audio to create a breakthrough spatial listening experience. CustomTune technology personalizes your sound automatically to your ears' shape.",
        "attributes": {
            "anc": "Bose CustomTune Active Noise Cancellation",
            "battery": "Up to 24 hours of listening time",
            "bluetooth": "Bluetooth 5.3 with SimpleSync",
            "spatial_audio": "Bose Immersive Audio mode",
            "materials": "Plush protein leather earcups, cast aluminum arms"
        },
        "images": [
            "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&auto=format&fit=crop"
        ],
        "tags": ["bose", "headphones", "quietcomfort", "anc", "travel", "bestseller"]
    },

    # ─── ELECTRONICS: Cameras & Wearables ───────────────────
    {
        "category": "electronics",
        "subcategory": "Cameras & Optics",
        "title": "Sony Alpha A7 IV Full-Frame Mirrorless Interchangeable Lens Camera (Body Only)",
        "brand": "Sony",
        "price": 2498.00,
        "compare_at_price": 2699.00,
        "stock": 20,
        "short_description": "33MP BSI full-frame sensor, 4K 60p 10-bit 4:2:2, real-time eye autofocus for humans, animals, and birds.",
        "description": "With groundbreaking performance in both still and movie recording, the α7 IV is the ideal hybrid camera, providing breathtaking imagery alongside on-the-spot delivery and distribution. The 33MP Exmor R sensor combined with the BIONZ XR processing engine delivers high speed and exquisite image quality.",
        "attributes": {
            "sensor": "33MP Full-Frame Exmor R CMOS BSI Sensor",
            "processor": "BIONZ XR Image Processor",
            "video": "4K 60p 10-bit 4:2:2 recording, S-Cinetone",
            "autofocus": "759-point Fast Hybrid AF with Real-time Eye AF",
            "stabilization": "5-axis steady shot optical in-body image stabilization",
            "viewfinder": "3.68m-Dot OLED EVF with 120 fps refresh rate"
        },
        "images": [
            "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&auto=format&fit=crop"
        ],
        "tags": ["sony", "camera", "mirrorless", "photography", "video", "4k", "pro"]
    },
    {
        "category": "electronics",
        "subcategory": "Smart Home & Wearables",
        "title": "Apple Watch Series 9 GPS 45mm (Midnight Aluminum Case with Sport Band)",
        "brand": "Apple",
        "price": 429.00,
        "compare_at_price": 459.00,
        "stock": 70,
        "short_description": "S9 SiP chip, Double Tap gesture control, brighter 2000-nit display, ECG and Blood Oxygen apps.",
        "description": "Smarter. Brighter. Mightier. Apple Watch Series 9 helps you stay connected, active, healthy, and safe. Featuring double tap, a magical way to interact with Apple Watch without touching the screen, an even brighter display, and Precision Finding for iPhone.",
        "attributes": {
            "chip": "S9 SiP with 64-bit dual-core processor, 4-core Neural Engine",
            "display": "Always-On Retina OLED (up to 2000 nits, down to 1 nit)",
            "health_sensors": "Blood Oxygen, ECG, Temperature sensing, Heart Rate",
            "water_resistance": "50m swimproof (WR50)",
            "battery": "18 hours normal use, up to 36 hours in Low Power Mode"
        },
        "images": [
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop"
        ],
        "tags": ["apple", "watch", "smartwatch", "fitness", "health", "bestseller"]
    },
    {
        "category": "electronics",
        "subcategory": "Smart Home & Wearables",
        "title": "Nintendo Switch OLED Model with White Joy-Con",
        "brand": "Nintendo",
        "price": 349.99,
        "compare_at_price": 379.99,
        "stock": 90,
        "short_description": "Vibrant 7-inch OLED screen, wide adjustable stand, wired LAN dock, 64GB internal storage.",
        "description": "Meet the newest member of the Nintendo Switch family. Play at home on the TV or on-the-go with a vibrant 7-inch OLED screen with the Nintendo Switch (OLED model). In addition to a new screen with vivid colors and sharp contrast, the Nintendo Switch – OLED Model includes a wide adjustable stand for more comfortable viewing angles.",
        "attributes": {
            "screen": "7.0-inch OLED capacitive multi-touch (1280x720)",
            "storage": "64GB internal (expandable with microSD up to 2TB)",
            "battery_life": "Approx. 4.5 to 9 hours",
            "modes": "TV mode, Tabletop mode, Handheld mode",
            "dock": "Includes wired LAN port, HDMI port, 2 USB ports"
        },
        "images": [
            "https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=800&auto=format&fit=crop"
        ],
        "tags": ["nintendo", "switch", "gaming", "console", "portable", "bestseller"]
    },

    # ─── FASHION & APPAREL ──────────────────────────────────
    {
        "category": "fashion",
        "subcategory": "Sneakers & Footwear",
        "title": "Nike Air Force 1 '07 All-White Classic Leather Sneakers",
        "brand": "Nike",
        "price": 115.00,
        "compare_at_price": 130.00,
        "stock": 120,
        "short_description": "Crisp leather edges, stitched overlays, heritage Nike Air cushioning, timeless low-cut design.",
        "description": "The radiance lives on in the Nike Air Force 1 '07, the b-ball icon that puts a fresh spin on what you know best: crisp leather, bold colors and the perfect amount of flash to make you shine. Stitched overlays on the upper add heritage style, durability and support, while Nike Air cushioning adds lightweight, all-day comfort.",
        "attributes": {
            "upper": "100% Genuine Full-Grain Leather",
            "midsole": "Nike Air encapsulated cushioning unit",
            "outsole": "Non-marking solid rubber with pivot circles",
            "closure": "Lace-up with metallic AF-1 dubrae",
            "colorway": "Triple White (White/White)"
        },
        "images": [
            "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=800&auto=format&fit=crop"
        ],
        "tags": ["nike", "airforce", "sneakers", "shoes", "streetwear", "classic", "bestseller"]
    },
    {
        "category": "fashion",
        "subcategory": "Sneakers & Footwear",
        "title": "Adidas Ultraboost Light Running Shoes - Core Black / Cloud White",
        "brand": "Adidas",
        "price": 189.99,
        "compare_at_price": 210.00,
        "stock": 75,
        "short_description": "Light BOOST midsole with 30% lighter material, Primeknit+ upper, Continental rubber grip.",
        "description": "Experience epic energy with the new Ultraboost Light, our lightest Ultraboost ever. The magic lies in the Light BOOST midsole, a new generation of adidas BOOST. Its unique molecule design achieves the lightest BOOST foam to date and boasts a 10% lower carbon footprint than previous models.",
        "attributes": {
            "midsole": "Light BOOST cushioning technology",
            "upper": "Primeknit+ FORGED textile made with 50% Parley Ocean Plastic",
            "outsole": "Continental™ Better Rubber outsole",
            "weight": "299g (Size 9)",
            "drop": "10mm (heel: 30mm / forefoot: 20mm)"
        },
        "images": [
            "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800&auto=format&fit=crop"
        ],
        "tags": ["adidas", "ultraboost", "running", "shoes", "sneakers", "fitness", "bestseller"]
    },
    {
        "category": "fashion",
        "subcategory": "Jackets & Outerwear",
        "title": "The North Face 1996 Retro Nuptse 700-Fill Down Jacket - TNF Black",
        "brand": "The North Face",
        "price": 330.00,
        "compare_at_price": 360.00,
        "stock": 45,
        "short_description": "700-fill goose down insulation, durable water-repellent (DWR) finish, packable hood.",
        "description": "Built for mountain- and city-life, the 1996 Retro Nuptse Jacket has an unmistakable silhouette. With its water-repellent ripstop fabric and oversized baffles filled with ultra-warm 700-fill goose down, it keeps you warm and dry when temperatures plunge.",
        "attributes": {
            "insulation": "700-fill goose down certified to the Responsible Down Standard (RDS)",
            "fabric": "40D 54 g/m² 100% recycled nylon ripstop with non-PFC DWR finish",
            "hood": "Stows in collar",
            "packability": "Stows in right hand pocket",
            "fit": "Relaxed boxy silhouette"
        },
        "images": [
            "https://images.unsplash.com/photo-1544441893-675973e31985?w=800&auto=format&fit=crop"
        ],
        "tags": ["thenorthface", "jacket", "winter", "puffer", "outerwear", "streetwear", "bestseller"]
    },
    {
        "category": "fashion",
        "subcategory": "Jackets & Outerwear",
        "title": "Patagonia Better Sweater 1/4-Zip Fleece Jacket - Stonewash",
        "brand": "Patagonia",
        "price": 139.00,
        "compare_at_price": 159.00,
        "stock": 60,
        "short_description": "100% recycled polyester sweater-knit fleece dyed with low-impact process, Fair Trade Certified sewn.",
        "description": "A warm, low-bulk quarter-zip pullover made with soft, ribbed-knit 100% recycled polyester fleece. Dyed with a low-impact process that significantly reduces the use of dyestuffs, energy and water compared to conventional dyeing methods.",
        "attributes": {
            "material": "10-oz 100% recycled polyester knit fleece",
            "features": "Quarter-zip with zip-through stand-up collar",
            "pocket": "Zippered left-chest pocket",
            "certifications": "Fair Trade Certified™ sewn, bluesign® approved fabric"
        },
        "images": [
            "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=800&auto=format&fit=crop"
        ],
        "tags": ["patagonia", "fleece", "jacket", "sustainable", "outdoors", "bestseller"]
    },
    {
        "category": "fashion",
        "subcategory": "Jeans & Trousers",
        "title": "Levi's 501 Original Fit Straight Leg Selvedge Denim Jeans",
        "brand": "Levi's",
        "price": 98.00,
        "compare_at_price": 118.00,
        "stock": 85,
        "short_description": "The original straight fit jean since 1873, iconic signature button fly, 100% non-stretch cotton denim.",
        "description": "Close your eyes. Think “jeans.” Now open. They were 501s, right? With a classic straight leg and iconic styling, they're literally the blueprint for every pair of jeans in existence — burned into the world's collective cortex ever since Levi Strauss invented them in 1873.",
        "attributes": {
            "fit": "Regular through the thigh with straight leg opening",
            "fabric": "100% Cotton heavy-duty denim",
            "fly": "Signature metal button fly",
            "wash": "Medium Indigo Stone Wash"
        },
        "images": [
            "https://images.unsplash.com/photo-1542272604-780c96856592?w=800&auto=format&fit=crop"
        ],
        "tags": ["levis", "jeans", "denim", "classic", "vintage", "501", "bestseller"]
    },
    {
        "category": "fashion",
        "subcategory": "Eyewear & Accessories",
        "title": "Ray-Ban Original Wayfarer Polarized Sunglasses (Tortoise Frame / Green Classic G-15)",
        "brand": "Ray-Ban",
        "price": 221.00,
        "compare_at_price": 245.00,
        "stock": 50,
        "short_description": "100% UV protection, high quality polarized crystal lenses, iconic acetate frame.",
        "description": "Ray-Ban Original Wayfarer Classics are the most recognizable style in the history of sunglasses. Since its initial design in 1952, Wayfarer Classics gained popularity among celebrities, musicians, artists and those with an impeccable fashion sense.",
        "attributes": {
            "lens_technology": "Polarized Crystal Green G-15 (absorbs 85% of visible light)",
            "frame_material": "Hypoallergenic Handcrafted Acetate",
            "dimensions": "Lens width: 50mm, Bridge: 22mm, Temple: 150mm",
            "uv_protection": "100% UVA/UVB protection (UV400)"
        },
        "images": [
            "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&auto=format&fit=crop"
        ],
        "tags": ["rayban", "sunglasses", "wayfarer", "polarized", "eyewear", "classic", "bestseller"]
    },

    # ─── HOME & KITCHEN ─────────────────────────────────────
    {
        "category": "home_kitchen",
        "subcategory": "Kitchen Appliances",
        "title": "Instant Pot Duo Plus 9-in-1 Multi-Cooker (6 Quart)",
        "brand": "Instant Pot",
        "price": 129.95,
        "compare_at_price": 149.95,
        "stock": 95,
        "short_description": "Pressure cooker, slow cooker, rice cooker, yogurt maker, steamer, sauté pan, sous vide, and food warmer.",
        "description": "The Instant Pot Duo Plus 9-in-1 is an upgrade to America's #1 most-loved multi-cooker. Easy to use, easy to clean, versatile and convenient. The improved easy-release steam switch makes venting steam simple, fast, and whisper-quiet. Cook delicious meals up to 70% faster than traditional methods.",
        "attributes": {
            "capacity": "6 Quart (serves up to 6 people)",
            "functions": "9-in-1 (Pressure, Slow Cook, Rice, Yogurt, Steam, Sauté, Sous Vide, Sterilize, Warm)",
            "inner_pot": "Food-grade 18/8 stainless steel cooking pot with tri-ply bottom",
            "safety": "Over 10 proven safety features including Overheat Protection™",
            "power": "1000 Watts"
        },
        "images": [
            "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800&auto=format&fit=crop"
        ],
        "tags": ["instantpot", "kitchen", "cooker", "appliance", "sousvide", "bestseller"]
    },
    {
        "category": "home_kitchen",
        "subcategory": "Kitchen Appliances",
        "title": "Nespresso VertuoPlus Deluxe Coffee and Espresso Machine by De'Longhi",
        "brand": "Nespresso",
        "price": 199.00,
        "compare_at_price": 229.00,
        "stock": 60,
        "short_description": "Centrifusion extraction technology, single-touch brewing, 5 cup sizes from espresso to alto.",
        "description": "Nespresso VertuoPlus offers freshly brewed coffee with crema as well as delicious, authentic espresso. Designed for Nespresso Vertuo capsules only, with smart barcode recognition technology that adjusts brewing parameters automatically for each unique blend.",
        "attributes": {
            "technology": "Centrifusion™ technology (7,000 RPM capsule spinning)",
            "cup_sizes": "Espresso (1.35oz), Double Espresso (2.7oz), Gran Lungo (5oz), Coffee (7.7oz), Alto (14oz)",
            "water_tank": "60 oz extra-large movable water reservoir",
            "heat_up_time": "Fast 20-second preheating"
        },
        "images": [
            "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&auto=format&fit=crop"
        ],
        "tags": ["nespresso", "coffee", "espresso", "latte", "kitchen", "delonghi", "bestseller"]
    },
    {
        "category": "home_kitchen",
        "subcategory": "Cleaning & Vacuums",
        "title": "Dyson V15 Detect Absolute Cordless Stick Vacuum Cleaner",
        "brand": "Dyson",
        "price": 749.99,
        "compare_at_price": 849.99,
        "stock": 35,
        "short_description": "Laser reveals invisible dust, piezo sensor measures dust particles, 240AW powerful suction.",
        "description": "Dyson's most intelligent cordless vacuum. A precisely-angled laser illuminates invisible dust on hard floors. An acoustic piezo sensor continuously sizes and counts dust particles, automatically increasing suction power when higher volumes of debris are detected. The LCD screen shows real-time scientific proof of a deep clean.",
        "attributes": {
            "suction_power": "240 Air Watts with Dyson Hyperdymium™ motor (125,000 RPM)",
            "run_time": "Up to 60 minutes fade-free power",
            "filtration": "Whole-machine advanced HEPA filtration (traps 99.99% of particles down to 0.1 microns)",
            "bin_volume": "0.2 Gallons (0.77 Liters) with point-and-shoot hygienic emptying",
            "weight": "3.1 kg (6.8 lbs)"
        },
        "images": [
            "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800&auto=format&fit=crop"
        ],
        "tags": ["dyson", "vacuum", "cleaning", "cordless", "laser", "home", "bestseller"]
    },
    {
        "category": "home_kitchen",
        "subcategory": "Cookware & Dining",
        "title": "Le Creuset Enameled Cast Iron Signature Round Dutch Oven (5.5 Quart, Cerise Red)",
        "brand": "Le Creuset",
        "price": 420.00,
        "compare_at_price": 460.00,
        "stock": 30,
        "short_description": "Handcrafted in France since 1925, superior heat distribution and retention, chip-resistant enamel.",
        "description": "An iconic culinary classic, the Le Creuset Round Dutch Oven is indispensable in the kitchens of home cooks and professional chefs alike. Expertly crafted from enameled cast iron, the everyday versatility of the Dutch oven makes it ideal for everything from slow-cooking and braising to roasting, baking, frying and more.",
        "attributes": {
            "capacity": "5.5 Quart (serves 5-6)",
            "origin": "Handcrafted in Fresnoy-le-Grand, France",
            "compatibility": "Induction, Gas, Electric, Ceramic, Halogen, Oven safe up to 500°F",
            "material": "Vibrant exterior enamel resists chipping and cracking; sand-colored interior enamel promotes caramelization",
            "cleaning": "Dishwasher safe"
        },
        "images": [
            "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=800&auto=format&fit=crop"
        ],
        "tags": ["lecreuset", "cookware", "dutchoven", "castiron", "cooking", "french", "luxury"]
    },
    {
        "category": "home_kitchen",
        "subcategory": "Ergonomic Furniture",
        "title": "Herman Miller Aeron Ergonomic Office Chair (Size B, Graphite Frame with PostureFit SL)",
        "brand": "Herman Miller",
        "price": 1495.00,
        "compare_at_price": 1695.00,
        "stock": 25,
        "short_description": "Breathable 8Z Pellicle elastomeric suspension, PostureFit SL adjustable spinal support, tilt limiter.",
        "description": "The benchmark for ergonomic seating since its introduction in 1994, Aeron combines human-centered design with state-of-the-art materials. Engineered with 8Z Pellicle mesh across the seat and back to eliminate pressure points, and adjustable PostureFit SL pads that stabilize the sacrum and support the lumbar region of the spine.",
        "attributes": {
            "size": "Size B (Medium - Fits majority of heights 5'3\" to 6'2\")",
            "suspension": "8Z Pellicle breathable elastomeric mesh with 8 distinct zones of tension",
            "support": "Adjustable PostureFit SL spinal stabilization",
            "adjustments": "Fully adjustable arms (height, depth, pivot), forward seat angle, tilt limiter",
            "warranty": "12-Year Herman Miller Manufacturer Warranty"
        },
        "images": [
            "https://images.unsplash.com/photo-1580481077197-2856230f2495?w=800&auto=format&fit=crop"
        ],
        "tags": ["hermanmiller", "aeron", "officechair", "ergonomic", "desk", "workspace", "luxury"]
    },

    # ─── BEAUTY & PERSONAL CARE ─────────────────────────────
    {
        "category": "beauty",
        "subcategory": "Hair Styling & Care",
        "title": "Dyson Airwrap Multi-Styler Complete Long (Nickel/Copper)",
        "brand": "Dyson",
        "price": 599.99,
        "compare_at_price": 649.99,
        "stock": 40,
        "short_description": "Dries and styles simultaneously using Coanda airflow, no extreme heat damage, 6 versatile attachments.",
        "description": "Style with air, not extreme heat. The Dyson Airwrap multi-styler harnesses an aerodynamic phenomenon called the Coanda effect to attract and wrap hair to the barrel, or surface of the brush. Powered by the Dyson digital motor V9, with intelligent heat control measuring air temperature over 40 times a second to ensure it stays below 302°F.",
        "attributes": {
            "motor": "Dyson digital motor V9 (110,000 RPM creating 3.2kPa pressure)",
            "heat_control": "Intelligent thermistor measurement prevents heat damage",
            "attachments": "1.2\" & 1.6\" Coanda long barrels, Firm & Soft smoothing brushes, Round volumizing brush, Coanda smoothing dryer",
            "hair_types": "Engineered for multiple hair types, chest-length or longer"
        },
        "images": [
            "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800&auto=format&fit=crop"
        ],
        "tags": ["dyson", "airwrap", "hairstyling", "curler", "beauty", "luxury", "bestseller"]
    },
    {
        "category": "beauty",
        "subcategory": "Skincare Treatments",
        "title": "La Mer Crème de la Mer Ultra-Rich Moisturizing Cream (2 oz / 60ml)",
        "brand": "La Mer",
        "price": 380.00,
        "compare_at_price": 410.00,
        "stock": 35,
        "short_description": "Cell-renewing Miracle Broth™, deep soothing hydration, visibly diminishes lines and wrinkles.",
        "description": "The legendary moisturizing cream that started it all. Born from the sea, this legendary cream has the power to transform the skin. In a short time, firmness improves, lines, wrinkles and the look of pores become less visible, skin looks virtually ageless. With cell-renewing Miracle Broth™ and antioxidant Lime Tea.",
        "attributes": {
            "volume": "60 ml / 2 fl. oz.",
            "key_ingredient": "Miracle Broth™ (fermented sea kelp, vitamins, minerals, wheat germ, eucalyptus)",
            "benefits": "Deep healing hydration, barrier soothing, age defense",
            "skin_type": "Ideal for drier skin types"
        },
        "images": [
            "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=800&auto=format&fit=crop"
        ],
        "tags": ["lamer", "cremedelamer", "skincare", "moisturizer", "luxury", "antiaging"]
    },
    {
        "category": "beauty",
        "subcategory": "Fragrances & Perfumes",
        "title": "Dior Sauvage Eau de Parfum Spray for Men (3.4 oz / 100ml)",
        "brand": "Dior",
        "price": 165.00,
        "compare_at_price": 185.00,
        "stock": 65,
        "short_description": "Radiant Calabrian bergamot, smoky Papua New Guinean vanilla absolute, sensually woody trail.",
        "description": "Dior Sauvage Eau de Parfum exudes sensual and mysterious facets. Calabrian bergamot adds its signature juicy freshness. Spicy notes lend fullness and sensuality, as the fragrance is enveloped in the smoky accents of Papua New Guinean vanilla absolute for greater virility. Inspired by the magic hour of twilight in the desert.",
        "attributes": {
            "volume": "100 ml / 3.4 oz",
            "fragrance_family": "Earthy & Woody",
            "scent_type": "Warm Woods with Fresh Citrus",
            "notes": "Reggio Bergamot, Sichuan Pepper, Ambroxan, Papua New Guinean Vanilla"
        },
        "images": [
            "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=800&auto=format&fit=crop"
        ],
        "tags": ["dior", "sauvage", "cologne", "perfume", "fragrance", "men", "luxury", "bestseller"]
    },

    # ─── SPORTS & OUTDOORS ──────────────────────────────────
    {
        "category": "sports_outdoors",
        "subcategory": "Fitness Equipment",
        "title": "Bowflex SelectTech 552 Adjustable Dumbbells (Pair, 5 to 52.5 lbs)",
        "brand": "Bowflex",
        "price": 429.00,
        "compare_at_price": 549.00,
        "stock": 40,
        "short_description": "Replaces 15 sets of weights with selector dial system, space-efficient home gym training.",
        "description": "These adjustable dumbbells replace 15 sets of weights. Weights adjust from 5 to 52.5 lbs in 2.5 lb increments up to the first 25 lbs. Easy-to-use selection dials for adjusting weights smoothly. Say goodbye to 15 sets of dumbbells cluttering your workout space.",
        "attributes": {
            "weight_range": "5 to 52.5 lbs (2.3 to 23.8 kg) per dumbbell",
            "increments": "2.5 lb increments for the first 25 lbs, then 5 lb increments",
            "dimensions": "16.9\" L x 8.3\" W x 9\" H each",
            "molding": "Durable molding around metal plates for smooth lift-off and quieter workouts"
        },
        "images": [
            "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800&auto=format&fit=crop"
        ],
        "tags": ["bowflex", "dumbbells", "fitness", "weights", "homegym", "strength", "bestseller"]
    },
    {
        "category": "sports_outdoors",
        "subcategory": "Yoga & Recovery",
        "title": "Theragun PRO Plus Multi-Therapy Percussive Massage Device",
        "brand": "Therabody",
        "price": 599.00,
        "compare_at_price": 649.00,
        "stock": 35,
        "short_description": "Deep 16mm percussive therapy, near-infrared LED light therapy, vibration therapy, biometric sensor.",
        "description": "The ultimate recovery device. Theragun PRO Plus combines deep tissue percussive therapy with near-infrared LED light therapy, vibration therapy, and thermal therapy. Scientifically proven to relieve pain, optimize mobility, and accelerate muscle recovery for world-class athletes and active individuals.",
        "attributes": {
            "amplitude": "16mm percussive depth reaches 60% deeper into muscle",
            "stall_force": "Up to 60 lbs of no-stall force",
            "therapies": "Percussive therapy, Near-infrared LED light, Heat therapy, Cold therapy compatible, Breathwork",
            "screen": "Full-color LCD with guided visual routines and biometric heart rate display"
        },
        "images": [
            "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&auto=format&fit=crop"
        ],
        "tags": ["theragun", "therabody", "massage", "recovery", "fitness", "therapy", "pro"]
    },
    {
        "category": "sports_outdoors",
        "subcategory": "GPS & Sports Watches",
        "title": "Garmin Forerunner 265 GPS Running Smartwatch with AMOLED Display",
        "brand": "Garmin",
        "price": 449.99,
        "compare_at_price": 499.99,
        "stock": 55,
        "short_description": "Vibrant 1.3\" AMOLED touchscreen, training readiness metric, wrist-based running dynamics, 13-day battery.",
        "description": "Plan your strategy with daily suggested workouts, course details and more on the race widget. Wake up to your morning report with HRV status to see health insights alongside an overview of sleep, recovery and training outlook. Features multi-band GNSS with SatIQ™ technology for superior positioning accuracy in challenging environments.",
        "attributes": {
            "display": "1.3\" AMOLED Touchscreen with Corning Gorilla Glass 4",
            "battery_life": "Up to 13 days in smartwatch mode, up to 20 hours in GPS mode",
            "gps": "Multi-band GNSS with SatIQ™ technology",
            "water_rating": "5 ATM (50 meters swimproof)",
            "music_storage": "Download songs and playlists from Spotify, Deezer or Amazon Music"
        },
        "images": [
            "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&auto=format&fit=crop"
        ],
        "tags": ["garmin", "running", "smartwatch", "gps", "marathon", "fitness", "bestseller"]
    },
    {
        "category": "sports_outdoors",
        "subcategory": "Outdoor & Camping",
        "title": "Yeti Tundra 45 Hard Cooler - Desert Tan",
        "brand": "Yeti",
        "price": 325.00,
        "compare_at_price": 350.00,
        "stock": 40,
        "short_description": "Rotomolded construction, PermaFrost 3-inch pressure-injected insulation, bear-resistant certification.",
        "description": "The YETI Tundra 45 combines versatility with legendary durability. Infused with that legendary YETI toughness — a durable rotomolded construction and up to three inches of PermaFrost™ Insulation. Which is all to say it's built to last and will keep your contents ice-cold even in sweltering triple-digit heat.",
        "attributes": {
            "capacity": "Holds up to 28 cans with recommended 2:1 ice-to-contents ratio",
            "insulation": "Up to 3 inches of commercial-grade PermaFrost™ polyurethane foam",
            "construction": "FatWall™ design rotomolded polyethylene (virtually indestructible)",
            "dimensions": "25 3/4\" L x 16 1/8\" W x 15 3/8\" H",
            "empty_weight": "23 lbs (10.4 kg)"
        },
        "images": [
            "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=800&auto=format&fit=crop"
        ],
        "tags": ["yeti", "cooler", "camping", "outdoors", "adventure", "icecold", "bestseller"]
    },

    # ─── FASHION: Quiet Luxury, Apparel & Accessories ──────────
    {
        "category": "fashion",
        "subcategory": "Jackets & Outerwear",
        "title": "Burberry The Pimlico Heritage Car Coat - Honey",
        "brand": "Burberry",
        "price": 1790.00,
        "compare_at_price": 1950.00,
        "stock": 20,
        "short_description": "Single-breasted cotton gabardine car coat tailored with clean raglan sleeves and Vintage check lining.",
        "description": "The Car Coat is a versatile, single-breasted style rooted in our motoring heritage. Light and protective, it is made in Castleford, Yorkshire from signature weatherproof cotton gabardine and lined in archival Vintage check — a print first used in the 1960s. The Pimlico fit is softly tailored with a straight cut that slips easily over tailored layers.",
        "attributes": {
            "material": "100% Weatherproof Cotton Gabardine",
            "lining": "100% Cotton Vintage Check Lining",
            "closure": "Concealed button placket, horn buttons",
            "fit": "Pimlico tailored fit",
            "origin": "Made in England"
        },
        "images": [
            "https://images.unsplash.com/photo-1544441893-675973e31985?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800&auto=format&fit=crop"
        ],
        "tags": ["burberry", "coat", "trench", "heritage", "luxury", "outerwear", "bestseller"]
    },
    {
        "category": "fashion",
        "subcategory": "Bags & Luggage",
        "title": "Burberry Small Two-Tone Canvas and Leather TB Bag",
        "brand": "Burberry",
        "price": 1950.00,
        "compare_at_price": 2100.00,
        "stock": 15,
        "short_description": "Structured canvas and smooth calf leather shoulder bag with Thomas Burberry Monogram clasp.",
        "description": "A structured silhouette in durable canvas and supple Italian-tanned topstitched leather, accented with a polished gold-plated Thomas Burberry Monogram clasp. Wear on the shoulder, crossbody, or carry as a clutch by detaching the adjustable leather strap.",
        "attributes": {
            "dimensions": "21 x 6 x 16 cm (8.3 x 2.4 x 6.3 in)",
            "outer": "92% Cotton, 8% Polyurethane with 100% Calf Leather trim",
            "hardware": "Polished gold-plated metal monogram clasp",
            "pockets": "One exterior slip pocket, one interior zip pocket",
            "strap": "Adjustable, detachable crossbody strap"
        },
        "images": [
            "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=800&auto=format&fit=crop"
        ],
        "tags": ["burberry", "bag", "handbag", "luxury", "leather", "crossbody", "quietluxury"]
    },
    {
        "category": "fashion",
        "subcategory": "Sneakers & Footwear",
        "title": "Burberry Cotton and Leather Webb Strap Sneakers",
        "brand": "Burberry",
        "price": 760.00,
        "compare_at_price": 820.00,
        "stock": 35,
        "short_description": "Monochrome slip-on leather sneakers with dual buckle straps and embossed Burberry lettering.",
        "description": "Crafted in Italy from ultra-soft optic white calf leather and breathable canvas lining, the Webb sneaker features statement double buckle straps across the vamp and subtle embossed lettering at the heel counter. Grounded on an ergonomic molded rubber sole.",
        "attributes": {
            "upper": "100% Calf Leather & Canvas",
            "sole": "100% Durable Ergonomic Rubber",
            "closure": "Dual buckle utility straps",
            "origin": "Made in Italy"
        },
        "images": [
            "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=800&auto=format&fit=crop"
        ],
        "tags": ["burberry", "sneakers", "footwear", "luxury", "minimalist", "white"]
    },
    {
        "category": "fashion",
        "subcategory": "Sneakers & Footwear",
        "title": "Loro Piana Summer Charms Walk Suede Loafers",
        "brand": "Loro Piana",
        "price": 1050.00,
        "compare_at_price": 1150.00,
        "stock": 25,
        "short_description": "Water-repellent unlined suede loafers adorned with mini padlock and charm hardware.",
        "description": "The quintessential quiet luxury footwear: handcrafted from unlined velvety calfskin suede treated with a water-repellent and stain-resistant finish. Complete with lightweight white latex soles and engraved metal charms resting across the front strap.",
        "attributes": {
            "material": "100% Unlined Calf Suede with water-repellent treatment",
            "sole": "Lightweight non-slip natural latex rubber",
            "detailing": "Engraved mini padlock and key charms",
            "origin": "Handmade in Italy"
        },
        "images": [
            "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=800&auto=format&fit=crop"
        ],
        "tags": ["loropiana", "loafers", "suede", "quietluxury", "luxury", "footwear", "italian"]
    },
    {
        "category": "fashion",
        "subcategory": "Jackets & Outerwear",
        "title": "Totême Signature Wool-Cashmere Blend Double Coat",
        "brand": "Totême",
        "price": 1280.00,
        "compare_at_price": 1400.00,
        "stock": 18,
        "short_description": "Oversized wrap silhouette woven from heavyweight brushed wool and cashmere with draped lapels.",
        "description": "A Scandinavian masterclass in minimalist proportion. Cut from an exceptionally soft blend of certified wool and cashmere, this double-breasted wrap coat features generous dropped shoulders, deep patch pockets, and a clean belted waist.",
        "attributes": {
            "composition": "90% Certified Wool, 10% Cashmere",
            "fit": "Signature relaxed, oversized silhouette",
            "color": "Oatmeal Melange",
            "care": "Dry clean only"
        },
        "images": [
            "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=800&auto=format&fit=crop"
        ],
        "tags": ["toteme", "coat", "wool", "cashmere", "minimalist", "scandinavian", "quietluxury"]
    },
    {
        "category": "fashion",
        "subcategory": "Bags & Luggage",
        "title": "Loewe Mini Puzzle Bag in Classic Calfskin - Tan",
        "brand": "Loewe",
        "price": 2450.00,
        "compare_at_price": 2600.00,
        "stock": 12,
        "short_description": "Cuboid shape with distinctive geometric puzzle cut lines, hand-painted edges and embossed Anagram.",
        "description": "Jonathan Anderson's debut bag for Loewe has achieved certified icon status. Its innovative cuboid silhouette is composed of 75 separate leather pieces assembled by hand, allowing the bag to fold completely flat or expand to hold daily essentials.",
        "attributes": {
            "leather": "Classic Spanish Calfskin with herringbone cotton canvas lining",
            "hardware": "Palladium metallic hardware",
            "strap": "Detachable and adjustable leather strap (115 cm drop)",
            "origin": "Artisanal handcrafting in Madrid, Spain"
        },
        "images": [
            "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=800&auto=format&fit=crop"
        ],
        "tags": ["loewe", "puzzle", "handbag", "designer", "leather", "luxury", "tan"]
    },
    {
        "category": "fashion",
        "subcategory": "Eyewear & Accessories",
        "title": "Saint Laurent SL 557 Shade Bold Acetate Sunglasses",
        "brand": "Saint Laurent",
        "price": 495.00,
        "compare_at_price": 530.00,
        "stock": 40,
        "short_description": "Narrow rectangular thick acetate sunglasses with bevelled temples and 100% UVA/UVB mineral lenses.",
        "description": "Infuse sleek Parisian edge into every look. These statement rectangular frames are carved from thick glossy black Italian acetate, featuring silver corner rivets and laser-engraved Saint Laurent signature branding along the wide temple arms.",
        "attributes": {
            "frame": "100% Premium Gloss Italian Acetate",
            "lenses": "100% UVA/UVB Category 3 Mineral Glass lenses",
            "dimensions": "Lens 53mm, Bridge 20mm, Temple 145mm",
            "case": "Includes magnetic Saint Laurent leather case and cloth"
        },
        "images": [
            "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&auto=format&fit=crop"
        ],
        "tags": ["saintlaurent", "sunglasses", "eyewear", "acetate", "luxury", "black"]
    },

    # ─── HOME & KITCHEN: Gourmet & Ergonomics ───────────────────
    {
        "category": "home_kitchen",
        "subcategory": "Cookware & Dining",
        "title": "Le Creuset Enameled Cast Iron Round Dutch Oven (5.5 Qt, Cerise Red)",
        "brand": "Le Creuset",
        "price": 420.00,
        "compare_at_price": 460.00,
        "stock": 30,
        "short_description": "Iconic French enameled cast iron Dutch oven with sand-colored interior and stainless steel knob.",
        "description": "An indispensable heirloom culinary classic. Individually cast in sand molds and hand-inspected by French artisans since 1925, Le Creuset's iconic Dutch oven delivers peerless heat distribution and moisture retention for slow-cooking, braising, baking sourdough, and searing.",
        "attributes": {
            "capacity": "5.5 Quarts (Serves 5–6)",
            "material": "Enameled Cast Iron, chip-resistant vibrant porcelain enamel",
            "heat_rating": "Oven safe up to 500°F (260°C)",
            "cooktop_compatibility": "Induction, Gas, Electric, Ceramic, Halogen",
            "origin": "Handcrafted in Fresnoy-le-Grand, France"
        },
        "images": [
            "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800&auto=format&fit=crop"
        ],
        "tags": ["lecreuset", "cookware", "dutchoven", "castiron", "gourmet", "kitchen", "bestseller"]
    },
    {
        "category": "home_kitchen",
        "subcategory": "Kitchen Appliances",
        "title": "Fellow Stagg EKG Electric Pour-Over Kettle - Matte Black",
        "brand": "Fellow",
        "price": 195.00,
        "compare_at_price": 220.00,
        "stock": 50,
        "short_description": "Precision gooseneck spout, to-the-degree PID temperature control, and built-in brew stopwatch.",
        "description": "Elevate your morning ritual. Whether you're a seasoned barista or a coffee enthusiast, the Fellow Stagg EKG combines aesthetic perfection with surgical pouring control. Featuring a 1200W quick-heating element, full PID temperature regulation from 135°F to 212°F, and a 60-minute temperature hold mode.",
        "attributes": {
            "volume": "0.9 Liters (30 oz)",
            "power": "1200W, 120V fast-boil heating system",
            "spout": "Counterbalanced precision gooseneck pour spout",
            "display": "High-contrast discreet LCD showing target and live temperatures"
        },
        "images": [
            "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=800&auto=format&fit=crop"
        ],
        "tags": ["fellow", "kettle", "pourover", "coffee", "design", "kitchen", "bestseller"]
    },
    {
        "category": "home_kitchen",
        "subcategory": "Kitchen Appliances",
        "title": "Breville The Barista Touch Impress Espresso Machine - Brushed Stainless Steel",
        "brand": "Breville",
        "price": 1499.95,
        "compare_at_price": 1699.95,
        "stock": 16,
        "short_description": "Touchscreen guidance, assisted 22lb tamping with auto dose, and Auto MilQ microfoam texturing.",
        "description": "Third-wave specialty coffee made effortless at home. The Barista Touch Impress guides you with step-by-step touchscreen feedback, intelligent dosing, assisted precision tamping, and automated silky microfoam calibrated for dairy, almond, oat, and soy milks.",
        "attributes": {
            "heating_system": "ThermoJet system with 3-second rapid warm-up",
            "grinder": "Precision Baratza European hardened steel burrs with 30 grind settings",
            "tamping": "Assisted Impress puck system with 7-degree barista twist and 22 lbs force",
            "milk_system": "Auto MilQ temperature and texture control (Hands-free)"
        },
        "images": [
            "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&auto=format&fit=crop"
        ],
        "tags": ["breville", "espresso", "coffee", "barista", "kitchen", "premium", "bestseller"]
    },
    {
        "category": "home_kitchen",
        "subcategory": "Ergonomic Furniture",
        "title": "Herman Miller Aeron Ergonomic Office Chair (Size B, Graphite, PostureFit SL)",
        "brand": "Herman Miller",
        "price": 1725.00,
        "compare_at_price": 1895.00,
        "stock": 22,
        "short_description": "Pellicle 8Z breathable suspension mesh, dual PostureFit SL sacral support, and fully adjustable arms.",
        "description": "The gold standard of ergonomic seating. Designed by Bill Stumpf and Don Chadwick, the Aeron chair distributes weight evenly across 8 variable tension zones, eliminating pressure points and keeping your body cool and comfortable through intensive 10+ hour work days.",
        "attributes": {
            "size": "Medium (Size B, accommodates 5'2\" to 6'2\" users)",
            "support": "PostureFit SL adjustable sacral and lumbar pads",
            "tilt": "Forward tilt (5°) and tilt limiter with tension control",
            "arms": "Fully adjustable 4D armrests (height, depth, and pivot)",
            "warranty": "12-Year Herman Miller 24/7 use manufacturer warranty"
        },
        "images": [
            "https://images.unsplash.com/photo-1580481077194-c79326e5e80a?w=800&auto=format&fit=crop"
        ],
        "tags": ["hermanmiller", "aeron", "officechair", "ergonomic", "furniture", "luxury", "homeoffice"]
    },
    {
        "category": "home_kitchen",
        "subcategory": "Cleaning & Vacuums",
        "title": "Dyson V15 Detect Absolute Cordless Stick Vacuum",
        "brand": "Dyson",
        "price": 749.99,
        "compare_at_price": 849.99,
        "stock": 35,
        "short_description": "Illuminating green laser Reveals invisible dust, piezo sensor measures particle count, 230AW suction.",
        "description": "Dyson's most intelligent cordless vacuum. Features a laser slim Fluffy cleaner head that reveals microscopic dust on hard floors, an acoustic piezo sensor that continuously sizes and counts particles, automatically adjusting suction power according to debris volume.",
        "attributes": {
            "suction_power": "230 Air Watts (Hyperdymium motor spinning up to 125,000 rpm)",
            "run_time": "Up to 60 minutes fade-free click-in battery",
            "filtration": "Whole-machine HEPA filtration traps 99.99% of particles down to 0.1 microns",
            "bin_capacity": "0.76 Liters with hygienic point-and-shoot emptying"
        },
        "images": [
            "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800&auto=format&fit=crop"
        ],
        "tags": ["dyson", "vacuum", "cleaning", "home", "smart", "laser", "bestseller"]
    },

    # ─── BEAUTY & PERSONAL CARE: Luxury Skincare & Scent ────────
    {
        "category": "beauty",
        "subcategory": "Skincare Treatments",
        "title": "Augustinus Bader The Rich Cream with TFC8® (50ml)",
        "brand": "Augustinus Bader",
        "price": 290.00,
        "compare_at_price": 310.00,
        "stock": 40,
        "short_description": "Award-winning cellular renewal daily moisturizer powered by biomedical TFC8® technology.",
        "description": "Backed by 30 years of research by biomedical scientist Professor Augustinus Bader. The Rich Cream is an intensely luxurious moisturizer that deeply hydrates, reduces fine lines and wrinkles, and visibly promotes cellular renewal with evening primrose, argan, and avocado oils.",
        "attributes": {
            "active_technology": "Trigger Factor Complex 8 (TFC8®) amino acids, vitamins, and synthesized molecules",
            "skin_type": "Ideal for normal to dry skin, mature skin, and dry winter climates",
            "volume": "50 ml / 1.7 fl. oz. recyclable glass pump",
            "formula": "100% vegan, cruelty-free, fragrance-free"
        },
        "images": [
            "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=800&auto=format&fit=crop"
        ],
        "tags": ["augustinusbader", "skincare", "richcream", "luxury", "antiaging", "cleanbeauty", "bestseller"]
    },
    {
        "category": "beauty",
        "subcategory": "Fragrances & Perfumes",
        "title": "Maison Francis Kurkdjian Baccarat Rouge 540 Eau de Parfum (70ml)",
        "brand": "Maison Francis Kurkdjian",
        "price": 325.00,
        "compare_at_price": 350.00,
        "stock": 30,
        "short_description": "Luminous amber, floral, and woody breeze with jasmine, saffron, cedarwood, and ambergris.",
        "description": "An intoxicating, iconic signature fragrance born of the encounter between Maison Francis Kurkdjian and Baccarat to celebrate the crystal manufacturer's 250th birthday. Luminous and sophisticated, Baccarat Rouge 540 lays on the skin like an amber, floral, and woody breeze.",
        "attributes": {
            "olfactory_family": "Woody Amber Floral",
            "top_notes": "Grandiflorum Jasmine from Egypt, Saffron",
            "heart_notes": "Bitter Almond from Morocco, Cedarwood",
            "base_notes": "Ambergris accord, Woody Musk",
            "size": "70 ml / 2.4 fl. oz. Spray Flacon"
        },
        "images": [
            "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=800&auto=format&fit=crop"
        ],
        "tags": ["mfk", "perfume", "baccaratrouge", "fragrance", "luxury", "french", "bestseller"]
    },
    {
        "category": "beauty",
        "subcategory": "Fragrances & Perfumes",
        "title": "Le Labo Santal 33 Eau de Parfum (100ml)",
        "brand": "Le Labo",
        "price": 320.00,
        "compare_at_price": 340.00,
        "stock": 35,
        "short_description": "Hypnotic scent of the American West featuring Australian sandalwood, cedarwood, cardamom, and leather.",
        "description": "A perfume that touches the sensual universality of this icon, which would intoxicate a man as much as a woman. It introduces Le Labo's use of cardamom, iris, violet, and ambrox which crackle in the formula and bring to this smoking wood alloy (Australian sandalwood, cedarwood) spicy, leathery, and musky notes.",
        "attributes": {
            "profile": "Woody, Aromatic, Spicy Leather",
            "concentration": "Eau de Parfum (Hand-formulated)",
            "volume": "100 ml / 3.4 fl. oz.",
            "ethical": "Cruelty-free, paraben-free, 100% vegan"
        },
        "images": [
            "https://images.unsplash.com/photo-1547887537-6158d64c35b3?w=800&auto=format&fit=crop"
        ],
        "tags": ["lelabo", "santal33", "fragrance", "perfume", "niche", "artisanal", "bestseller"]
    },
    {
        "category": "beauty",
        "subcategory": "Hair Styling & Care",
        "title": "Dyson Airwrap Multi-Styler Complete Long - Strawberry Bronze and Blush Pink",
        "brand": "Dyson",
        "price": 599.99,
        "compare_at_price": 649.99,
        "stock": 25,
        "short_description": "Coanda airflow technology styles hair without extreme heat damage; engineered for long hair.",
        "description": "Curl, wave, smooth, and dry with no extreme heat. The Dyson Airwrap utilizes an aerodynamic phenomenon known as the Coanda effect, curving air to attract and wrap hair around the barrel using only air and controlled heat.",
        "attributes": {
            "heat_control": "Intelligent glass bead thermistor measuring air temperature 40 times a second",
            "motor": "Dyson digital motor V9 spinning at 110,000 rpm",
            "attachments": "Includes 6 re-engineered styling attachments and travel pouch",
            "hair_length": "Optimized for hair that's chest-length or longer"
        },
        "images": [
            "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800&auto=format&fit=crop"
        ],
        "tags": ["dyson", "airwrap", "hairstyling", "beauty", "haircare", "luxury", "bestseller"]
    },

    # ─── SPORTS & OUTDOORS: Performance Athletics ───────────────
    {
        "category": "sports_outdoors",
        "subcategory": "Outdoor & Camping",
        "title": "Arc'teryx Beta AR Gore-Tex Pro Waterproof Shell Jacket - Black",
        "brand": "Arc'teryx",
        "price": 600.00,
        "compare_at_price": 650.00,
        "stock": 30,
        "short_description": "Most Rugged 3-layer GORE-TEX PRO waterproof jacket with helmet-compatible DropHood™.",
        "description": "Packable, breathable, durable waterproof protection across the spectrum of alpine environments and activities. The Beta AR Jacket is engineered with GORE-TEX PRO with Most Rugged Technology — a next-generation material developed in collaboration with Gore.",
        "attributes": {
            "fabric": "N40d 3L GORE-TEX PRO with ultra-durable N80d reinforcements",
            "hood": "Helmet-compatible DropHood™ with Cohaesive™ cord locks",
            "zippers": "WaterTight™ external zippers and pit zips for rapid ventilation",
            "recco": "Integrated RECCO® reflector for search and rescue location"
        },
        "images": [
            "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&auto=format&fit=crop"
        ],
        "tags": ["arcteryx", "goretex", "jacket", "waterproof", "alpine", "outdoor", "bestseller"]
    },
    {
        "category": "sports_outdoors",
        "subcategory": "Fitness Equipment",
        "title": "On Cloudmonster 2 Max-Cushion Road Running Shoes - Undyed White",
        "brand": "On Running",
        "price": 179.99,
        "compare_at_price": 190.00,
        "stock": 45,
        "short_description": "Extreme CloudTec® cushioning with dual-density Helion™ superfoam and nylon Speedboard®.",
        "description": "Maximum energy return with monstrous cushioning. The Cloudmonster 2 brings On's biggest Cloud elements ever, combined with an ultra-responsive nylon blend Speedboard® to propel you forward on long recovery runs and tempo sessions alike.",
        "attributes": {
            "cushioning": "Max-Cushion CloudTec® with dual-density Helion™ superfoam",
            "drop": "6 mm heel-to-toe drop",
            "weight": "295 g (10.4 oz)",
            "sustainability": "100% recycled polyester engineered mesh upper"
        },
        "images": [
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop"
        ],
        "tags": ["onrunning", "cloudmonster", "runningshoes", "sneakers", "marathon", "fitness", "bestseller"]
    },
    {
        "category": "sports_outdoors",
        "subcategory": "Yoga & Recovery",
        "title": "Lululemon Align High-Rise Pant 25\" - Black",
        "brand": "Lululemon",
        "price": 98.00,
        "compare_at_price": 118.00,
        "stock": 60,
        "short_description": "Buttery-soft, weightless Nulu™ fabric engineered for yoga and low-impact mindful movement.",
        "description": "When feeling nothing is everything. The iconic Align collection, powered by Nulu™ fabric, is so weightless and buttery-soft, all you feel is your practice. Featuring four-way stretch, sweat-wicking performance, and an interior waistband pocket for keys.",
        "attributes": {
            "fabric": "81% Nylon, 19% Lycra® elastane Nulu™ textile",
            "rise_inseam": "High-Rise fit, 25-inch ankle inseam length",
            "waistband": "Seamless lie-flat contour waistband with hidden card pocket",
            "feel": "Weightless, buttery-soft second-skin compression"
        },
        "images": [
            "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&auto=format&fit=crop"
        ],
        "tags": ["lululemon", "align", "leggings", "yoga", "activewear", "fitness", "bestseller"]
    },

    # ─── ELECTRONICS: Premium Audio, Imaging & Smart ────────────
    {
        "category": "electronics",
        "subcategory": "Audio & Headphones",
        "title": "Sony WH-1000XM5 Wireless Industry-Leading Noise-Canceling Headphones - Silver",
        "brand": "Sony",
        "price": 399.99,
        "compare_at_price": 449.99,
        "stock": 50,
        "short_description": "Auto NC Optimizer, two processors, 8 microphones, 30-hour battery, and LDAC Hi-Res Wireless.",
        "description": "Sony's flagship noise-canceling headphones rewrite the rules for distraction-free listening. Featuring two processors controlling eight microphones, an Auto NC Optimizer for automatically calibrating noise cancellation based on wearing conditions and atmospheric pressure, and an ultra-comfortable lightweight design.",
        "attributes": {
            "driver_unit": "30mm precision-engineered Carbon Fiber composite driver",
            "noise_canceling": "Integrated Processor V1 + HD Noise Canceling Processor QN1",
            "battery_life": "30 hours with ANC turned on; 3 min quick-charge gives 3 hours playback",
            "connectivity": "Bluetooth 5.2 with Multipoint connection, LDAC Hi-Res Audio, 3.5mm wired"
        },
        "images": [
            "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&auto=format&fit=crop"
        ],
        "tags": ["sony", "headphones", "noisecanceling", "bluetooth", "audio", "premium", "bestseller"]
    },
    {
        "category": "electronics",
        "subcategory": "Cameras & Optics",
        "title": "Fujifilm X100VI Digital Camera - Silver",
        "brand": "Fujifilm",
        "price": 1599.00,
        "compare_at_price": 1799.00,
        "stock": 10,
        "short_description": "40.2MP X-Trans CMOS 5 HR sensor, 6.0-stop in-body image stabilization, 20 Film Simulation modes.",
        "description": "The ultimate daily documentary camera. Merging timeless analog dial operations with Fujifilm's cutting-edge 40.2-megapixel sensor, 6-stop 5-axis IBIS, and 6.2K video recording, all packed into a compact all-aluminum body that slips effortlessly into any jacket pocket.",
        "attributes": {
            "sensor": "40.2MP back-illuminated X-Trans CMOS 5 HR sensor",
            "lens": "Fujinon 23mm F2.0 II fixed prime lens (35mm equivalent)",
            "stabilization": "5-axis In-Body Image Stabilization up to 6.0 stops",
            "viewfinder": "Advanced Hybrid Viewfinder (Optical OVF + 3.69M dot OLED EVF)",
            "film_simulations": "20 modes including REALA ACE, Classic Chrome, and Nostalgic Neg"
        },
        "images": [
            "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&auto=format&fit=crop"
        ],
        "tags": ["fujifilm", "x100vi", "camera", "photography", "classic", "vintage", "bestseller"]
    },
    {
        "category": "electronics",
        "subcategory": "Smart Home & Wearables",
        "title": "Apple Watch Ultra 2 (GPS + Cellular 49mm Titanium Case with Orange Ocean Band)",
        "brand": "Apple",
        "price": 799.00,
        "compare_at_price": 849.00,
        "stock": 30,
        "short_description": "Rugged 49mm aerospace-grade titanium case, 3000-nit display, S9 SiP chip, precision dual-frequency GPS.",
        "description": "The most rugged and capable Apple Watch ever. Crafted from lightweight corrosion-resistant aerospace titanium with raised sapphire crystal edges, 100m water resistance with EN13319 dive certification, and up to 72 hours of battery life in Low Power Mode.",
        "attributes": {
            "case": "49mm Aerospace-grade Titanium with customizable Action button",
            "display": "Always-On Retina display with up to 3000 nits peak brightness",
            "chip": "S9 SiP with 64-bit dual-core processor and Double Tap gesture",
            "battery_life": "Up to 36 hours normal use; up to 72 hours in Low Power Mode",
            "water_resistance": "100m water resistant, depth gauge with water temperature sensor"
        },
        "images": [
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop"
        ],
        "tags": ["apple", "applewatch", "ultra2", "smartwatch", "fitness", "titanium", "bestseller"]
    }
]

