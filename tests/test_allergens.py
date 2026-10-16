import pytest
from src.rules import find_guest_allergens


def meal(*ingredients):
    return {"id": "t1", "name": "Test Meal", "ingredients": list(ingredients)}


def types(m):
    return {f["allergen_type"] for f in find_guest_allergens(m)}


def test_salmon_is_fish():
    m = meal("Salmon (SALMON (SALMO SALAR), WATER, SALT, COLOR ADDED)")
    findings = find_guest_allergens(m)
    assert types(m) == {"fish"}
    assert findings[0]["evidence"].lower().startswith("salmon")


def test_cashews_are_tree_nut():
    assert types(meal("Cashews (CASHEWS, CANOLA OIL, SEA SALT)")) == {"tree_nut"}


def test_peanut_butter_is_peanut():
    assert types(meal("Peanut Butter")) == {"peanut"}


def test_walnut_halves_and_garlic_pepper_still_flagged():
    m = meal("Garlic Pepper (SPICES INCLUDING PEPPER)", "Walnut Halves")
    assert types(m) == {"tree_nut"}


def test_shrimp_is_shellfish():
    assert types(meal("Shrimp")) == {"shellfish"}


def test_fish_sauce_is_fish():
    assert types(meal("Fish Sauce")) == {"fish"}


def test_pine_nut_in_pesto_is_tree_nut():
    assert types(meal("Pesto (BASIL, PINE NUTS, PARMESAN)")) == {"tree_nut"}


@pytest.mark.parametrize("ingredient", [
    "Jerk Sauce (PINEAPPLE JUICE, ALLSPICE, NUTMEG, HOT PEPPERS)",
    "Butternut Squash",
    "Multicolor Sesame Seeds (SESAME SEED)",
    "Sweetened Flaked Coconut (COCONUT, SUGAR)",
    "Red Pepper Pesto (ROASTED RED PEPPER, SUNFLOWER SEEDS)",
    "Sliced Green Onions (SCALLIONS)",
    "Oyster Mushrooms",
    "Chicken Broth Concentrate (CHICKEN STOCK, SALT)",
])
def test_no_false_positives(ingredient):
    assert find_guest_allergens(meal(ingredient)) == []