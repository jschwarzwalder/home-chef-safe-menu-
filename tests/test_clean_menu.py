"""Tests for Home Chef menu cleaning and normalization."""
import json
from pathlib import Path

import src.clean_menu as clean_menu_module

from src.clean_menu import (
    clean_ingredient,
    clean_meal,
    clean_menu,
    create_scan_text,
    fetch_meal_details,
    get_detailed_ingredients,
    get_meal_amount,
    get_meal_type,
    get_tier,
    is_included,
)


def make_meal(
    *,
    meal_id=1001,
    title="Test Chicken",
    meal_type="Entree",
    tier="Fresh Start",
    servings=None,
    ingredients=None,
    recipe_url=None,
):
    """Create a minimal Home Chef-style meal for testing."""
    meal = {
        "id": meal_id,
        "title": title,
        "menu_category_and_color": {
            "label": meal_type,
        },
        "meal_label": {
            "label": tier,
        },
        "ingredients": ingredients or [
            {"name": "Chicken Breasts"},
            {"name": "Potatoes"},
        ],
    }

    if servings is not None:
        meal["servings"] = servings

    if recipe_url is not None:
        meal["recipe_url"] = recipe_url

    return meal

def load_sample_menu():
    """Load the real sample Home Chef menu fixture."""
    path = Path(__file__).parent / "fixtures" / "sample-menu.json"

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def test_get_meal_type_returns_category():
    """Meal type should come from menu_category_and_color."""
    meal = make_meal(meal_type="Family")

    assert get_meal_type(meal) == "Family"


def test_get_meal_type_defaults_when_missing():
    """Missing meal category should produce a known fallback."""
    meal = {"menu_category_and_color": {}}

    assert get_meal_type(meal) == "Unknown Type"


def test_get_tier_returns_label():
    """Meal tier should come from meal_label."""
    meal = make_meal(tier="Culinary Collection")

    assert get_tier(meal) == "Culinary Collection"


def test_get_tier_defaults_when_missing():
    """Missing meal tier should produce a known fallback."""
    meal = {"meal_label": {}}

    assert get_tier(meal) == "Unknown Tier"


def test_family_meal_is_always_four_servings():
    """Family meals should always be treated as four servings."""
    meal = make_meal(meal_type="Family", servings=2)

    assert get_meal_amount(meal) == 4


def test_family_tier_is_always_four_servings():
    """A meal labeled Family should always be treated as four servings."""
    meal = make_meal(tier="Family", servings=2)

    assert get_meal_amount(meal) == 4


def test_explicit_servings_are_preserved():
    """Explicit serving information should be used when available."""
    meal = make_meal(servings=4)

    assert get_meal_amount(meal) == 4


def test_string_servings_are_converted_to_integer():
    """String serving values should be converted to integers."""
    meal = make_meal(servings="4")

    assert get_meal_amount(meal) == 4


def test_missing_servings_default_to_two():
    """Meals without serving information should default to two."""
    meal = make_meal()

    assert get_meal_amount(meal) == 2


def test_get_meal_amount_family_tier_overrides_requested_amount():
    """Family tier should force four servings regardless of requested amount."""
    meal = make_meal(tier="Family", servings=2)

    assert get_meal_amount(meal) == 4


def test_get_meal_amount_family_type_overrides_requested_amount():
    """Family meal type should force four servings regardless of requested amount."""
    meal = make_meal(meal_type="Family", servings=2)

    assert get_meal_amount(meal) == 4


def test_get_meal_amount_string_family_servings_are_ignored():
    """Family meals should still resolve to four servings when source value is a string."""
    meal = make_meal(meal_type="Family", servings="2")

    assert get_meal_amount(meal) == 4


def test_get_meal_amount_zero_servings():
    """Zero should not silently become the default if explicitly supplied."""
    meal = make_meal(servings=0)

    assert get_meal_amount(meal) == 0


def test_excluded_tier_is_not_included():
    """Premium meals should be excluded."""
    meal = make_meal(tier="Premium")

    assert is_included(meal, 2) is False


def test_excluded_meal_type_is_not_included():
    """Excluded meal categories should not be included."""
    meal = make_meal(meal_type="Dessert")

    assert is_included(meal, 2) is False


def test_wrong_serving_amount_is_not_included():
    """A meal with the wrong serving count should be excluded."""
    meal = make_meal(servings=4)

    assert is_included(meal, 2) is False


def test_matching_standard_two_serving_meal_is_included():
    """A normal two-serving meal should be included."""
    meal = make_meal(servings=2)

    assert is_included(meal, 2) is True


def test_clean_ingredient_returns_name():
    """Ingredient cleaning should retain only the ingredient name."""
    ingredient = {
        "name": "Butter",
        "amount": "2 oz.",
        "allergens": ["milk"],
    }

    assert clean_ingredient(ingredient) == "Butter"


def test_clean_ingredient_ignores_missing_name():
    """Ingredients without names should be discarded."""
    ingredient = {
        "amount": "2 oz.",
        "allergens": [],
    }

    assert clean_ingredient(ingredient) is None


def test_clean_ingredient_with_empty_name_is_discarded():
    """Empty ingredient names should be discarded."""
    ingredient = {
        "name": "",
        "amount": "2 oz.",
        "allergens": [],
    }

    assert clean_ingredient(ingredient) is None


def test_clean_ingredient_with_none_name_is_discarded():
    """None ingredient names should be discarded."""
    ingredient = {
        "name": None,
        "amount": "2 oz.",
        "allergens": [],
    }

    assert clean_ingredient(ingredient) is None


def test_clean_meal_normalizes_core_fields(monkeypatch):
    """clean_meal should produce the compact meal representation."""
    meal = make_meal(
        meal_id=1234,
        title="Garlic Chicken",
        meal_type="Entree",
        tier="Fresh Start",
        servings=2,
        recipe_url="https://www.homechef.com/meals/garlic-chicken",
    )

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: {
            "ingredients": [
                {
                    "name": "Chicken Breasts",
                    "amount": "12 oz.",
                    "allergens": [],
                },
                {
                    "name": "Butter",
                    "amount": "2 oz.",
                    "allergens": ["milk"],
                },
            ]
        },
    )

    result = clean_meal(meal)

    assert result == {
        "id": 1234,
        "name": "Garlic Chicken",
        "type": "Entree",
        "tier": "Fresh Start",
        "servings": 2,
        "ingredients": [
            "Chicken Breasts",
            "Butter",
        ],
        "recipe_url": "https://www.homechef.com/meals/garlic-chicken",
    }


def test_clean_meal_does_not_preserve_unwanted_metadata(monkeypatch):
    """clean_meal should intentionally produce a compact representation."""
    meal = make_meal(
        ingredients=[
            {
                "name": "Chicken",
                "amount": "12 oz.",
                "allergens": ["milk"],
                "photo": "huge-image-url",
            }
        ],
    )

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    result = clean_meal(meal)

    assert result == {
        "id": 1001,
        "name": "Test Chicken",
        "type": "Entree",
        "tier": "Fresh Start",
        "servings": 2,
        "ingredients": ["Chicken"],
    }


def test_clean_meal_falls_back_to_original_ingredients(monkeypatch):
    """Original menu ingredients should be used when detail lookup fails."""
    meal = make_meal(
        ingredients=[
            {"name": "Chicken"},
            {"name": "Rice"},
        ],
    )

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    result = clean_meal(meal)

    assert result["ingredients"] == ["Chicken", "Rice"]


def test_clean_meal_uses_detailed_ingredients_when_available(monkeypatch):
    """Detailed API ingredients should replace the basic menu ingredients."""
    meal = make_meal(
        ingredients=[
            {"name": "Chicken"},
        ],
    )

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: {
            "ingredients": [
                {"name": "Chicken"},
                {"name": "Seasoning Blend"},
                {"name": "Natural Flavors"},
            ]
        },
    )

    result = clean_meal(meal)

    assert result["ingredients"] == [
        "Chicken",
        "Seasoning Blend",
        "Natural Flavors",
    ]


def test_clean_meal_preserves_recipe_url_when_present(monkeypatch):
    """Recipe URL should be retained when supplied."""
    meal = make_meal(
        recipe_url="https://www.homechef.com/meals/test-chicken",
    )

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    result = clean_meal(meal)

    assert result["recipe_url"] == (
        "https://www.homechef.com/meals/test-chicken"
    )


def test_clean_meal_omits_recipe_url_when_missing(monkeypatch):
    """Recipe URL should not be added when the source meal has none."""
    meal = make_meal()

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    result = clean_meal(meal)

    assert "recipe_url" not in result


def test_clean_meal_discards_extra_homechef_metadata(monkeypatch):
    """Cleaning should retain only the compact fields we explicitly support."""
    meal = make_meal(
        title="Boom Boom Turkey Rice Bowl",
        servings=4,
    )

    meal.update(
        {
            "subtitle": "with stir-fried vegetables",
            "description": "A quick family-friendly turkey rice bowl.",
            "filterable_tags": ["Easy-Prep"],
            "meal_option_groups": [
                {
                    "id": "WPea7mPk",
                    "title": "Pick your protein",
                    "meal_options": [],
                }
            ],
        }
    )

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    result = clean_meal(meal)

    assert result == {
        "id": 1001,
        "name": "Boom Boom Turkey Rice Bowl",
        "type": "Entree",
        "tier": "Fresh Start",
        "servings": 4,
        "ingredients": [
            "Chicken Breasts",
            "Potatoes",
        ],
    }


def test_clean_meal_empty_detail_ingredients_falls_back_to_original(
    monkeypatch,
):
    """An empty detail ingredient list should fall back to menu ingredients."""
    meal = make_meal(
        ingredients=[
            {"name": "Chicken"},
            {"name": "Rice"},
        ],
    )

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: {"ingredients": []},
    )

    result = clean_meal(meal)

    assert result["ingredients"] == ["Chicken", "Rice"]


def test_clean_meal_detail_response_without_ingredients_falls_back(
    monkeypatch,
):
    """A detail response without an ingredients key should fall back."""
    meal = make_meal(
        ingredients=[
            {"name": "Chicken"},
            {"name": "Rice"},
        ],
    )

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: {},
    )

    result = clean_meal(meal)

    assert result["ingredients"] == ["Chicken", "Rice"]

def test_get_detailed_ingredients_discards_empty_detail_entries(monkeypatch):
    """Empty entries in detailed ingredients should be discarded."""

    meal = make_meal(
        ingredients=[
            {"name": "Chicken"},
        ],
    )

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: {
            "ingredients": [
                {"name": "Chicken"},
                None,
                {"name": "Rice"},
            ]
        },
    )

    result = get_detailed_ingredients(meal)

    assert result == [
        {"name": "Chicken"},
        {"name": "Rice"},
    ]

def test_fetch_meal_details_returns_json_response(monkeypatch):
    """Successful detail requests should return decoded JSON."""

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

        def read(self):
            return b'{"ingredients": [{"name": "Chicken"}]}'

    monkeypatch.setattr(
        "src.clean_menu.urllib.request.urlopen",
        lambda request, timeout: FakeResponse(),
    )

    result = fetch_meal_details(1234)

    assert result == {
        "ingredients": [
            {"name": "Chicken"},
        ]
    }

def test_get_detailed_ingredients_without_meal_id_uses_menu_ingredients():
    """Missing meal IDs should use the ingredients already in the menu."""
    meal = {
        "title": "Chicken Dinner",
        "ingredients": [
            {"name": "Chicken"},
            {"name": "Rice"},
            {"name": ""},
            {"amount": "2 oz."},
        ],
    }

    result = get_detailed_ingredients(meal)

    assert result == ["Chicken", "Rice"]

def test_clean_meal_discards_unnamed_detailed_ingredients(monkeypatch):
    """Unnamed ingredients from detailed data should not appear in the result."""
    meal = make_meal()

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: {
            "ingredients": [
                {"name": "Chicken"},
                {"amount": "2 oz."},
                {"name": ""},
                {"name": "Rice"},
            ]
        },
    )

    result = clean_meal(meal)

    assert result["ingredients"] == ["Chicken", "Rice"]

def test_fetch_meal_details_returns_none_when_request_fails(monkeypatch, capsys):
    """Failed detail requests should return None and print a warning."""

    def fake_urlopen(*args, **kwargs):
        raise OSError("network unavailable")

    monkeypatch.setattr(
        clean_menu_module.urllib.request,
        "urlopen",
        fake_urlopen,
    )

    result = clean_menu_module.fetch_meal_details(1234)

    assert result is None

    captured = capsys.readouterr()

    assert "Warning: could not fetch details for 1234" in captured.out
    assert "network unavailable" in captured.out

def test_fetch_meal_details_handles_request_error(monkeypatch, capsys):
    """Failed detail requests should return None and print a warning."""

    def fake_urlopen(*args, **kwargs):
        raise OSError("network unavailable")

    monkeypatch.setattr(
        clean_menu_module.urllib.request,
        "urlopen",
        fake_urlopen,
    )

    result = fetch_meal_details(1234)

    assert result is None

    captured = capsys.readouterr()

    assert "Warning: could not fetch details for 1234" in captured.out
    assert "network unavailable" in captured.out

def test_clean_menu_filters_excluded_and_wrong_serving_meals(monkeypatch):
    """clean_menu should return only eligible meals."""
    data = {
        "meals": [
            make_meal(
                meal_id=1,
                title="Safe Two Serving",
                servings=2,
            ),
            make_meal(
                meal_id=2,
                title="Four Serving",
                servings=4,
            ),
            make_meal(
                meal_id=3,
                title="Premium Meal",
                tier="Premium",
                servings=2,
            ),
            make_meal(
                meal_id=4,
                title="Dessert",
                meal_type="Dessert",
                servings=2,
            ),
        ]
    }

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    result = clean_menu(data, amount=2)

    assert [meal["id"] for meal in result] == [1]


def test_clean_menu_can_select_four_serving_meals(monkeypatch):
    """clean_menu should select Family/four-serving meals when requested."""
    data = {
        "meals": [
            make_meal(
                meal_id=1,
                title="Two Serving",
                servings=2,
            ),
            make_meal(
                meal_id=2,
                title="Family Meal",
                meal_type="Family",
                servings=4,
            ),
        ]
    }

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    result = clean_menu(data, amount=4)

    assert [meal["id"] for meal in result] == [2]
    assert result[0]["servings"] == 4


def test_clean_menu_handles_empty_menu(monkeypatch):
    """An empty menu should produce an empty result."""
    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    assert clean_menu({"meals": []}, amount=2) == []


def test_clean_menu_handles_missing_meals_key(monkeypatch):
    """Missing meals should be treated as an empty menu."""
    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    assert clean_menu({}, amount=2) == []


def test_clean_menu_does_not_fetch_details_for_excluded_meals(monkeypatch):
    """Excluded meals should be filtered before detail lookups occur."""
    data = {
        "meals": [
            make_meal(
                meal_id=1,
                title="Premium Meal",
                tier="Premium",
                servings=2,
            ),
            make_meal(
                meal_id=2,
                title="Valid Meal",
                servings=2,
            ),
        ]
    }

    fetched_ids = []

    def fake_fetch(meal_id):
        fetched_ids.append(meal_id)
        return None

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        fake_fetch,
    )

    result = clean_menu(data, amount=2)

    assert [meal["id"] for meal in result] == [2]
    assert fetched_ids == [2]


def test_clean_menu_does_not_fetch_details_for_wrong_servings(monkeypatch):
    """Meals with the wrong serving amount should not trigger detail lookups."""
    data = {
        "meals": [
            make_meal(
                meal_id=1,
                title="Four Serving Meal",
                servings=4,
            ),
            make_meal(
                meal_id=2,
                title="Two Serving Meal",
                servings=2,
            ),
        ]
    }

    fetched_ids = []

    def fake_fetch(meal_id):
        fetched_ids.append(meal_id)
        return None

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        fake_fetch,
    )

    result = clean_menu(data, amount=2)

    assert [meal["id"] for meal in result] == [2]
    assert fetched_ids == [2]


def test_clean_menu_preserves_input_order(monkeypatch):
    """Included meals should remain in their original menu order."""
    data = {
        "meals": [
            make_meal(meal_id=3, title="Third", servings=2),
            make_meal(meal_id=1, title="First", servings=2),
            make_meal(meal_id=2, title="Second", servings=2),
        ]
    }

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    result = clean_menu(data, amount=2)

    assert [meal["id"] for meal in result] == [3, 1, 2]


def test_create_scan_text_formats_meals_for_review():
    """Scan text should be compact and readable."""
    meals = [
        {
            "name": "Garlic Chicken",
            "type": "Entree",
            "tier": "Fresh Start",
            "ingredients": ["Chicken", "Potatoes", "Green Beans"],
        },
        {
            "name": "Steak Dinner",
            "type": "Entree",
            "tier": "Culinary Collection",
            "ingredients": ["Steak", "Butter"],
        },
    ]

    result = create_scan_text(meals)

    assert result == (
        "Garlic Chicken | Entree | Fresh Start\n"
        "Chicken; Potatoes; Green Beans\n\n"
        "Steak Dinner | Entree | Culinary Collection\n"
        "Steak; Butter"
    )


def test_create_scan_text_with_one_meal():
    """Scan text should work correctly with a single meal."""
    meals = [
        {
            "name": "Garlic Chicken",
            "type": "Entree",
            "tier": "Fresh Start",
            "ingredients": ["Chicken", "Potatoes"],
        }
    ]

    assert create_scan_text(meals) == (
        "Garlic Chicken | Entree | Fresh Start\n"
        "Chicken; Potatoes"
    )


def test_create_scan_text_with_empty_meals():
    """An empty meal list should produce empty scan text."""
    assert create_scan_text([]) == ""


def test_create_scan_text_with_empty_ingredients():
    """Meals without ingredients should still produce a valid header."""
    meals = [
        {
            "name": "Test Meal",
            "type": "Entree",
            "tier": "Fresh Start",
            "ingredients": [],
        }
    ]

    result = create_scan_text(meals)

    assert result == "Test Meal | Entree | Fresh Start\n"

def load_sample_menu():
    """Load the real sample Home Chef menu fixture."""
    path = Path(__file__).parent.parent / "tests" / "fixtures" / "sample-menu.json"

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_sample_menu_contains_meals():
    """The sample menu fixture should contain the expected source data."""
    data = load_sample_menu()

    assert "meals" in data
    assert len(data["meals"]) > 0


def test_sample_menu_cleaning_removes_excluded_meals(monkeypatch):
    """Cleaning the sample menu should remove excluded meal types and tiers."""

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    data = load_sample_menu()
    meals = clean_menu(data, amount=2)

    for meal in meals:
        assert meal["type"] not in clean_menu_module.EXCLUDED_LABELS
        assert meal["tier"] not in clean_menu_module.EXCLUDED_LABELS


def test_sample_menu_cleaning_keeps_only_requested_servings(monkeypatch):
    """Cleaned sample meals should all match the requested serving amount."""

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    data = load_sample_menu()
    meals = clean_menu(data, amount=2)

    assert meals

    for meal in meals:
        assert meal["servings"] == 2


def test_sample_menu_cleaning_contains_only_compact_meal_fields(
    monkeypatch,
):
    """Cleaned sample meals should contain only the supported compact fields."""

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    data = load_sample_menu()
    meals = clean_menu(data, amount=2)

    expected_fields = {
        "id",
        "name",
        "type",
        "tier",
        "servings",
        "ingredients",
    }

    for meal in meals:
        assert set(meal).issubset(expected_fields | {"recipe_url"})


def test_sample_menu_cleaning_contains_ingredient_names_only(monkeypatch):
    """Sample menu ingredients should be reduced to names."""

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    data = load_sample_menu()
    meals = clean_menu(data, amount=2)

    assert meals

    for meal in meals:
        for ingredient in meal["ingredients"]:
            assert isinstance(ingredient, str)
            assert ingredient


def test_sample_menu_cleaning_removes_ingredient_metadata(monkeypatch):
    """Ingredient amounts and other source metadata should not survive cleaning."""

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    data = load_sample_menu()
    meals = clean_menu(data, amount=2)

    assert meals

    for meal in meals:
        assert all(
            isinstance(ingredient, str)
            for ingredient in meal["ingredients"]
        )


def test_sample_menu_cleaning_preserves_meal_order(monkeypatch):
    """Eligible sample meals should remain in their original menu order."""

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    data = load_sample_menu()

    expected_ids = [
        meal["id"]
        for meal in data["meals"]
        if is_included(meal, 2)
    ]

    result = clean_menu(data, amount=2)

    assert [meal["id"] for meal in result] == expected_ids


def test_sample_menu_cleaning_produces_scan_text(monkeypatch):
    """The real sample menu should produce valid scan text."""

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    data = load_sample_menu()
    meals = clean_menu(data, amount=2)

    scan_text = create_scan_text(meals)

    assert isinstance(scan_text, str)

    if meals:
        assert scan_text

        for meal in meals:
            assert meal["name"] in scan_text
            assert meal["type"] in scan_text
            assert meal["tier"] in scan_text

def test_sample_menu_cleaning_returns_correct_two_serving_count(
    monkeypatch,
):
    """Cleaning the sample menu for 2 servings returns the expected count."""
    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    data = load_sample_menu()

    result = clean_menu(data, amount=2)

    assert len(result) == 4


def test_sample_menu_cleaning_returns_correct_four_serving_count(
    monkeypatch,
):
    """Cleaning the sample menu for 4 servings returns the expected count."""
    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    data = load_sample_menu()

    result = clean_menu(data, amount=4)

    assert len(result) == 3

def test_clean_sample_menu_returns_expected_two_serving_meals(
    monkeypatch,
):
    """Cleaning the sample menu should return the expected 2-serving meals."""

    data = load_sample_menu()

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    result = clean_menu(data, amount=2)

    assert len(result) == 4

    assert all(meal["servings"] == 2 for meal in result)


def test_clean_sample_menu_returns_expected_four_serving_meals(
    monkeypatch,
):
    """Cleaning the sample menu with amount=4 should return only 4-serving meals."""

    data = load_sample_menu()

    monkeypatch.setattr(
        "src.clean_menu.fetch_meal_details",
        lambda meal_id: None,
    )

    result = clean_menu(data, amount=4)

    assert len(result) == 3

    assert all(meal["servings"] == 4 for meal in result)