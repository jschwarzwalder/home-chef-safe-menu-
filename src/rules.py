"""
Ingredient-based exclusion rules for Home Chef meals.
"""

import re

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

GUEST_ALLERGENS = {
    "fish": [
        "salmon", "snapper", "tuna", "cod", "haddock", "halibut", "trout",
        "tilapia", "mahi-mahi", "mahi mahi", "bass", "catfish", "anchovy",
        "anchovies", "sardine", "mackerel", "herring", "pollock", "bonito",
        "fish",
    ],
    "shellfish": [
        "shrimp", "prawn", "crab", "lobster", "crayfish", "crawfish",
        "langoustine", "clam", "mussel", "oyster", "scallop", "squid",
        "octopus", "abalone",
    ],
    "peanut": ["peanut"],
    "tree_nut": [
        "almond", "cashew", "walnut", "pecan", "pistachio", "hazelnut",
        "filbert", "macadamia", "brazil nut", "pine nut", "pinenut",
    ],
}

HARD_BLOCKS = [
    "cream sauce base"
]

# Phrases that contain an allergen word but are not the allergen.
ALLERGEN_FALSE_POSITIVES = ["oyster mushroom", "crab apple"]

def is_excluded(text: str) -> bool:
    """
    Basic rule check (string-based for now).
    """
    text_lower = text.lower()

    for term in PEPPER_FAMILY + BELL_PEPPER + SAUCE_BLOCKLIST + HARD_BLOCKS:
        if term in text_lower:
            return True

    return False


def _compile(terms):
    return re.compile(
        r"\b(?:" + "|".join(re.escape(t) for t in terms) + r")s?\b",
        re.IGNORECASE,
    )


_ALLERGEN_PATTERNS = {k: _compile(v) for k, v in GUEST_ALLERGENS.items()}


def find_guest_allergens(meal: dict) -> list[dict]:
    """Return one finding per (ingredient, allergen_type) match."""
    findings = []
    for ingredient in meal.get("ingredients", []):
        text = ingredient
        for phrase in ALLERGEN_FALSE_POSITIVES:
            text = re.sub(re.escape(phrase), " ", text, flags=re.IGNORECASE)
        for allergen_type, pattern in _ALLERGEN_PATTERNS.items():
            match = pattern.search(text)
            if match:
                findings.append({
                    "allergen_type": allergen_type,
                    "evidence": ingredient,
                    "matched": match.group(0),
                    "location": "ingredient",
                })
    return findings

## For testing purposes, we will just return the meals unchanged for now.
def evaluate_meals(meals):
    """
    Temporary pass-through logic.
    For now: just return meals unchanged.
    We will implement filtering rules next.
    """
    return meals