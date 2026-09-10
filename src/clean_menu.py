"""
Create a compact, text scan of a Home Chef menu.

Keeps only:
    - meal name
    - meal type
    - tier
    - ingredient names

Intentionally omits:
    - amounts
    - allergens
    - IDs
    - instructions
    - images
    - nutrition
    - URLs
    - other API metadata

Usage:
    python src/clean_menu.py data/14-sep-2026.json

Output:
    data/14-sep-2026-scan.txt
"""

import json
import sys
from pathlib import Path


def clean_meal(meal):
    """Return the compact text representation of one meal."""

    menu_category = meal.get("menu_category_and_color") or {}
    meal_label = meal.get("meal_label") or {}

    name = meal.get("title") or "Unknown Meal"
    meal_type = menu_category.get("label") or "Unknown Type"
    tier = meal_label.get("label") or "Unknown Tier"

    ingredients = [
        ingredient.get("name")
        for ingredient in meal.get("ingredients", [])
        if ingredient.get("name")
    ]

    return (
        f"{name} | {meal_type} | {tier}\n"
        f"{'; '.join(ingredients)}"
    )


def clean_menu(data):
    """Convert the full Home Chef menu into compact text."""

    meals = data.get("meals", [])

    return "\n\n".join(
        clean_meal(meal)
        for meal in meals
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/clean_menu.py <input.json>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    output_path = input_path.with_name(
        f"{input_path.stem}-scan.txt"
    )

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = clean_menu(data)

    with output_path.open("w", encoding="utf-8") as f:
        f.write(cleaned)
        f.write("\n")

    original_size = input_path.stat().st_size
    cleaned_size = output_path.stat().st_size

    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    print(f"Meals:  {len(data.get('meals', []))}")
    print(f"Size:   {original_size:,} bytes → {cleaned_size:,} bytes")


if __name__ == "__main__":
    main()
