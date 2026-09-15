"""
NovaMart — Review Templates

Rating-weighted review generation with realistic J-curve distribution.
"""

import random

# Realistic J-shaped rating distribution
RATING_WEIGHTS = {5: 0.40, 4: 0.25, 3: 0.15, 2: 0.10, 1: 0.10}

REVIEW_TEMPLATES = {
    5: [
        {"title": "Exceeded all expectations!", "body": "I've been using the {product} for {period} now and I'm absolutely blown away. {positive}. Would definitely buy again!"},
        {"title": "Best purchase this year", "body": "The {product} is genuinely outstanding. {positive}. The build quality is exceptional and it performs even better than advertised."},
        {"title": "Worth every penny", "body": "After extensive research, I chose the {product} and couldn't be happier. {positive}. Highly recommend to anyone looking for quality."},
        {"title": "Amazing quality!", "body": "The {product} arrived in perfect condition and works flawlessly. {positive}. Five stars without hesitation."},
        {"title": "A game changer", "body": "This {product} has completely transformed my {use_case}. {positive}. I can't imagine going back to my old setup."},
    ],
    4: [
        {"title": "Great product with minor caveats", "body": "The {product} is really solid overall. {positive}. My only small complaint is {minor_negative}, but it doesn't detract from the experience."},
        {"title": "Very satisfied", "body": "I'm impressed with the {product}. {positive}. Could be perfect if they improved {minor_negative}, but still a great buy."},
        {"title": "Solid choice", "body": "The {product} delivers on its promises. {positive}. It's not perfect — {minor_negative} — but I'd still recommend it."},
        {"title": "Good value for money", "body": "For the price, the {product} is hard to beat. {positive}. {minor_negative}, but overall a sound investment."},
    ],
    3: [
        {"title": "Decent, but not amazing", "body": "The {product} is okay for the price. {neutral}. However, {negative}. It gets the job done but doesn't wow."},
        {"title": "Mixed feelings", "body": "I wanted to love the {product}, but {negative}. On the positive side, {positive}. It's average for its category."},
        {"title": "It's fine", "body": "The {product} works as described. {neutral}. Nothing special, nothing terrible. {negative} is worth noting though."},
    ],
    2: [
        {"title": "Disappointed", "body": "The {product} didn't meet my expectations. {negative}. {minor_positive}, but overall I'm not satisfied."},
        {"title": "Could be better", "body": "I had high hopes for the {product} but {negative}. The {minor_positive} is nice, but it doesn't make up for the issues."},
        {"title": "Not recommended", "body": "Save your money. The {product} {negative}. There are much better options in this price range."},
    ],
    1: [
        {"title": "Terrible experience", "body": "The {product} is awful. {negative}. Complete waste of money. Returning immediately."},
        {"title": "Don't buy this", "body": "I regret purchasing the {product}. {negative}. Zero redeeming qualities. Look elsewhere."},
        {"title": "Worst purchase ever", "body": "The {product} stopped working after {period}. {negative}. Incredibly frustrating experience."},
    ],
}

POSITIVE_COMMENTS = [
    "The build quality is exceptional — it feels premium in hand",
    "Performance is lightning fast, even under heavy workloads",
    "The design is sleek and modern, getting compliments everywhere",
    "Setup was incredibly easy, was up and running in minutes",
    "Customer support was responsive and helpful when I had questions",
    "The battery life is impressive, easily lasts the full day",
    "Sound quality is crystal clear with great bass response",
    "The display is stunning with vibrant, accurate colors",
    "Comfort level is outstanding, even after hours of use",
    "Features are well thought out and genuinely useful",
]

MINOR_NEGATIVE_COMMENTS = [
    "the packaging could be improved",
    "it's slightly heavier than expected",
    "the manual could use more detail",
    "the color is slightly different from the product photos",
    "it takes a moment to boot up initially",
    "the companion app could use some UI improvements",
]

NEGATIVE_COMMENTS = [
    "the quality feels cheap and flimsy",
    "it overheats during extended use",
    "the battery drains much faster than advertised",
    "it developed issues after just a few weeks",
    "the performance is sluggish and laggy",
    "it's nowhere near as good as the marketing claims",
    "the materials feel low-grade for this price point",
    "connectivity issues make it frustrating to use",
]

NEUTRAL_COMMENTS = [
    "It performs adequately for basic tasks",
    "The quality is acceptable for the price range",
    "It does what it says, nothing more nothing less",
    "The design is functional but unremarkable",
]

PERIODS = ["a week", "two weeks", "a month", "three months", "six months"]
USE_CASES = ["daily workflow", "home setup", "creative work", "fitness routine", "study sessions", "commute"]


def generate_review_text(rating: int, product_title: str) -> dict:
    """Generate a realistic review based on rating tier."""
    template = random.choice(REVIEW_TEMPLATES[rating])

    title = template["title"]
    body = template["body"].format(
        product=product_title,
        positive=random.choice(POSITIVE_COMMENTS),
        minor_positive=random.choice(POSITIVE_COMMENTS),
        minor_negative=random.choice(MINOR_NEGATIVE_COMMENTS),
        negative=random.choice(NEGATIVE_COMMENTS),
        neutral=random.choice(NEUTRAL_COMMENTS),
        period=random.choice(PERIODS),
        use_case=random.choice(USE_CASES),
    )

    return {"title": title, "body": body}


def pick_rating() -> int:
    """Pick a rating following the J-shaped distribution."""
    return random.choices(
        population=list(RATING_WEIGHTS.keys()),
        weights=list(RATING_WEIGHTS.values()),
        k=1,
    )[0]
