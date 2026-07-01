"""
Parses raw Home Chef menu text into structured meal objects.
"""
import re

TIER_KEYWORDS = {
    "PREMIUM",
    "CULINARY COLLECTION",
    "ONE SHEET PAN",
    "ONE PAN",
    "ONE POT",
    "FAMILY",
    "EXPRESS",
    "OVEN-READY",
    "FRESH START",
    "SUMMER PRODUCE"
}

PRICE_RE = re.compile(r"\$\d+\.\d+\s*/\s*(serving|pack|cookie skillet|bundle)?")
TIME_RE = re.compile(r"\d{1,2}-\d{1,2}\s*min")


def is_meal_start(line: str) -> bool:
    line = line.strip()

    if not line:
        return False

    if line in TIER_KEYWORDS:
        return True

    if PRICE_RE.search(line):
        return True

    return False


def extract_meals_from_text(raw_text: str):
    lines = [l.strip() for l in raw_text.splitlines()]
    meals = []
    current = []

    for line in lines:
        if is_meal_start(line):
            if current:
                meals.append(" ".join(current).strip())
                current = []

        current.append(line)

    if current:
        meals.append(" ".join(current).strip())

    return meals

def extract_from_html(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # STEP 1: find likely meal “cards”
    # (we will refine this once we inspect actual structure)

    candidates = soup.find_all(text=True)

    meals = []

    buffer = []
    for text in candidates:
        t = text.strip()
        if not t:
            continue

        buffer.append(t)

        if "Add To Order" in t:
            meals.append(" ".join(buffer))
            buffer = []

    return meals

def extract_meals(raw_text):
    """
    Extracts meal names and tiers from Home Chef page text.
    Ignores ingredients for now (intentional simplification).
    """

    lines = raw_text.splitlines()

    meals = []
    current_tier = None

    for i, line in enumerate(lines):
        clean = line.strip()

        if not clean:
            continue

        # Detect tier headers
        if any(tier in clean for tier in TIER_KEYWORDS):
            current_tier = clean
            continue

        # Heuristic: meal names are usually title case lines followed by "with ..."
        if current_tier:
            # skip prices, buttons, junk UI lines
            if (
                "$" in clean
                or "Add To Order" in clean
                or "Customize" in clean
                or "Pair with" in clean
                or "serving" in clean
                or "mins" in clean
                or "mins" in clean.lower()
            ):
                continue

            # Meal name detection heuristic
            if len(clean) > 5 and clean[0].isupper():
                meals.append({
                    "meal": clean,
                    "tier": current_tier
                })

    return meals

def parse_menu(raw_text: str):
    """
    Temporary parser placeholder.
    In v1 this will later extract:
    - meal name
    - tier
    - description block
    """
    meals = []

    lines = raw_text.split("\n")

    for line in lines:
        line = line.strip()

        # very naive placeholder logic
        if len(line) > 0:
            meals.append({
                "raw": line
            })

    return meals
