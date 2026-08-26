import json

from src.parser import parse_homechef_json


def load_sample_menu():
    with open("tests/fixtures/sample-menu.json", "r", encoding="utf-8") as f:
        return json.load(f)


def test_parse_homechef_json_returns_all_meals():
    data = load_sample_menu()

    meals = parse_homechef_json(data)

    assert len(meals) == 3


def test_parser_preserves_meal_metadata():
    data = load_sample_menu()

    meals = parse_homechef_json(data)

    meal = meals[0]

    assert meal["name"] == "Herbes de Provence Chicken"
    assert meal["subtitle"] == "with roasted potatoes and green beans"
    assert meal["tier"] == "Fresh Start"
    assert meal["prep_minutes"] == 35
    assert meal["spice_level"] == "Not Spicy"


def test_parser_preserves_ingredient_details():
    data = load_sample_menu()

    meals = parse_homechef_json(data)

    meal = meals[1]

    garlic_pepper = next(
        ingredient
        for ingredient in meal["ingredients"]
        if ingredient["name"] == "Garlic Pepper"
    )

    assert garlic_pepper["amount"] == "1 tsp."
    assert garlic_pepper["allergens"] == []


def test_parser_preserves_ingredient_allergens():
    data = load_sample_menu()

    meals = parse_homechef_json(data)

    meal = meals[2]

    shrimp = next(
        ingredient
        for ingredient in meal["ingredients"]
        if ingredient["name"] == "Shrimp"
    )

    assert shrimp["allergens"] == ["shellfish"]