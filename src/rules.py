"""
Ingredient-based exclusion rules for Home Chef meals.
"""

PEPPER_FAMILY = [
    "black pepper",
    "white pepper",
    "paprika",
    "chili",
    "chile",
    "jalapeño",
    "chipotle",
    "serrano",
    "ancho"
]

BELL_PEPPER = [
    "bell pepper"
]

SAUCE_BLOCKLIST = [
    "pesto",
    "bbq sauce",
    "chimichurri",
    "harissa",
    "katsu sauce",
    "marinara"
]

HARD_BLOCKS = [
    "cream sauce base"
]


def is_excluded(text: str) -> bool:
    """
    Basic rule check (string-based for now).
    """
    text_lower = text.lower()

    for term in PEPPER_FAMILY + BELL_PEPPER + SAUCE_BLOCKLIST + HARD_BLOCKS:
        if term in text_lower:
            return True

    return False

## For testing purposes, we will just return the meals unchanged for now.
def evaluate_meals(meals):
    """
    Temporary pass-through logic.
    For now: just return meals unchanged.
    We will implement filtering rules next.
    """
    return meals