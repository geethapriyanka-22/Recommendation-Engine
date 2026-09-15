"""
NovaMart — User Templates

Synthetic user profile generation with diverse names and locations.
"""

FIRST_NAMES = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn", "Avery",
    "Harper", "Emerson", "Rowan", "Sage", "Dakota", "Reese", "Finley", "Skyler",
    "Cameron", "Drew", "Jaden", "Parker", "Blake", "Hayden", "Logan", "Peyton",
    "Kai", "Nico", "Zara", "Mila", "Luna", "Ivy",
]

LAST_NAMES = [
    "Anderson", "Brooks", "Carter", "Davis", "Edwards", "Foster", "Garcia",
    "Hamilton", "Ibrahim", "Johnson", "Kim", "Lee", "Mitchell", "Nguyen",
    "O'Brien", "Patel", "Quinn", "Rivera", "Singh", "Thompson", "Ueda",
    "Vargas", "Williams", "Xu", "Yang", "Zhang", "Martinez", "Chen", "Ali", "Tanaka",
]

CITIES = [
    ("New York", "NY"), ("San Francisco", "CA"), ("Chicago", "IL"),
    ("Austin", "TX"), ("Seattle", "WA"), ("Boston", "MA"),
    ("Denver", "CO"), ("Portland", "OR"), ("Miami", "FL"),
    ("Atlanta", "GA"), ("Nashville", "TN"), ("Minneapolis", "MN"),
    ("San Diego", "CA"), ("Philadelphia", "PA"), ("Phoenix", "AZ"),
]

STREET_TEMPLATES = [
    "{num} {name} {suffix}",
]

STREET_NAMES = [
    "Oak", "Maple", "Cedar", "Pine", "Elm", "Birch", "Willow", "Sunset",
    "Highland", "Park", "Lake", "River", "Mountain", "Valley", "Harbor",
]

STREET_SUFFIXES = ["Street", "Avenue", "Boulevard", "Drive", "Lane", "Way", "Court", "Place"]

# Default seeded accounts
DEFAULT_ACCOUNTS = [
    {
        "email": "admin@novamart.com",
        "password": "Admin123!",
        "full_name": "Admin User",
        "role": "admin",
    },
    {
        "email": "seller@novamart.com",
        "password": "Seller123!",
        "full_name": "Seller Demo",
        "role": "seller",
    },
    {
        "email": "seller2@novamart.com",
        "password": "Seller123!",
        "full_name": "Marketplace Seller",
        "role": "seller",
    },
    {
        "email": "seller3@novamart.com",
        "password": "Seller123!",
        "full_name": "Premium Seller",
        "role": "seller",
    },
    {
        "email": "customer@novamart.com",
        "password": "Customer123!",
        "full_name": "Customer Demo",
        "role": "customer",
    },
]
