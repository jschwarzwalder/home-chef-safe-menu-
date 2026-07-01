"""
Classifies meals into SAFE, BORDERLINE, or NOT SAFE.
"""

from src.rules import is_excluded


def classify_meal(meal: dict) -> dict:
    """
    Takes a meal object and assigns a safety status.
    """

    raw_text = meal.get("raw", "")

    if is_excluded(raw_text):
        meal["status"] = "NOT SAFE"
    else:
        meal["status"] = "SAFE"

    return meal
