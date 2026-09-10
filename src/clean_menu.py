"""
Create compact Home Chef menu files for programmatic screening.

Keeps:
    - meal ID
    - meal name
    - meal type
    - tier
    - serving amount
    - ingredient names

Intentionally omits:
    - ingredient amounts
    - Home Chef allergen flags
    - instructions
    - images
    - nutrition
    - descriptions
    - other large API metadata

Default behavior:
    - 2-serving meals
    - excludes Premium
    - excludes Breakfast
    - excludes Heat & Eat
    - excludes Dessert
    - excludes Snack
    - excludes Side
    - excludes Mix & Match
    - excludes Protein
    - excludes Protein Pack

Family meals are always treated as 4-serving meals.

Usage:
    python src/clean_menu.py data/14-sep-2026.json

    python src/clean_menu.py data/14-sep-2026.json --amount 4

Outputs:
    data/14-sep-2026-clean.json
    data/14-sep-2026-scan.txt
"""

import argparse
import json
from pathlib import Path


EXCLUDED_LABELS = {
    "Premium",
    "Breakfast",
    "Heat & Eat",
    "Dessert",
    "Snack",
    "Side",
    "Mix & Match",
    "Protein",
    "Protein Pack",
}


def get_meal_amount(meal):
    """
    Determine the serving amount for a meal.

    Family meals are explicitly 4-serving meals.

    For other meals, try the source's serving information when
    available. If no usable serving information exists, default
    to 2 because standard Home Chef meals are normally 2-serving.
    """

    menu_category = meal.get("menu_category_and_color") or {}
    meal_label = meal.get("meal_label") or {}

    category = menu_category.get("label")
    label = meal_label.get("label")

    if category == "Family" or label == "Family":
        return 4

    # Check a few likely source fields without assuming that
    # every Home Chef response contains them.
    for key in (
        "servings",
        "serving_size",
        "num_servings",
        "number_of_servings",
    ):
        value = meal.get(key)

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                pass

    return 2


def get_meal_type(meal):
    """Return the Home Chef meal category/type."""

    menu_category = meal.get("menu_category_and_color") or {}
    return menu_category.get("label") or "Unknown Type"


def get_tier(meal):
    """Return the Home Chef meal tier/label."""

    meal_label = meal.get("meal_label") or {}
    return meal_label.get("label") or "Unknown Tier"


def is_included(meal, amount):
    """Return True when a meal belongs in the requested menu."""

    meal_type = get_meal_type(meal)
    tier = get_tier(meal)
    meal_amount = get_meal_amount(meal)

    if meal_type in EXCLUDED_LABELS:
        return False

    if tier in EXCLUDED_LABELS:
        return False

    return meal_amount == amount


def clean_ingredient(ingredient):
    """Keep only the ingredient name."""

    name = ingredient.get("name")

    if not name:
        return None

    return name


def clean_meal(meal):
    """Create the compact normalized representation of one meal."""

    ingredients = [
        name
        for ingredient in meal.get("ingredients", [])
        if (name := clean_ingredient(ingredient))
    ]

    cleaned = {
        "id": meal.get("id"),
        "name": meal.get("title") or "Unknown Meal",
        "type": get_meal_type(meal),
        "tier": get_tier(meal),
        "servings": get_meal_amount(meal),
        "ingredients": ingredients,
    }

    # Preserve the recipe URL when available. This is useful for
    # the eventual browser/ordering workflow and is much smaller
    # than preserving the rest of the API response.
    recipe_url = meal.get("recipe_url")

    if recipe_url:
        cleaned["recipe_url"] = recipe_url

    return cleaned


def clean_menu(data, amount):
    """Create the compact normalized menu."""

    meals = data.get("meals", [])

    return [
        clean_meal(meal)
        for meal in meals
        if is_included(meal, amount)
    ]


def create_scan_text(meals):
    """
    Create the compact text version used for pasting into ChatGPT.
    """

    sections = []

    for meal in meals:
        header = (
            f"{meal['name']} | "
            f"{meal['type']} | "
            f"{meal['tier']}"
        )

        ingredients = "; ".join(meal["ingredients"])

        sections.append(
            f"{header}\n{ingredients}"
        )

    return "\n\n".join(sections)


def main():
    parser = argparse.ArgumentParser(
        description="Create compact Home Chef menu files."
    )

    parser.add_argument(
        "input",
        help="Path to the Home Chef JSON file",
    )

    parser.add_argument(
        "--amount",
        type=int,
        choices=(2, 4),
        default=2,
        help="Number of servings wanted: 2 (default) or 4",
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"File not found: {input_path}")
        raise SystemExit(1)

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    meals = clean_menu(data, args.amount)

    json_output_path = input_path.with_name(
        f"{input_path.stem}-clean.json"
    )

    text_output_path = input_path.with_name(
        f"{input_path.stem}-scan.txt"
    )

    # Programmatic JSON output.
    with json_output_path.open("w", encoding="utf-8") as f:
        json.dump(
            {"meals": meals},
            f,
            indent=2,
            ensure_ascii=False,
        )
        f.write("\n")

    # ChatGPT-friendly text output.
    scan_text = create_scan_text(meals)

    with text_output_path.open("w", encoding="utf-8") as f:
        f.write(scan_text)
        f.write("\n")

    original_size = input_path.stat().st_size
    json_size = json_output_path.stat().st_size
    text_size = text_output_path.stat().st_size

    total_meals = len(data.get("meals", []))

    print(f"Input:       {input_path}")
    print(f"JSON output: {json_output_path}")
    print(f"Text output: {text_output_path}")
    print(f"Amount:      {args.amount}")
    print(f"Meals:       {len(meals)} of {total_meals}")
    print(
        f"JSON size:   {original_size:,} bytes → "
        f"{json_size:,} bytes"
    )
    print(f"Text size:   {text_size:,} bytes")


if __name__ == "__main__":
    main()
