"""
Builds final JSON output structure.
"""

import json


def build_output(meals: list) -> dict:
    """
    Converts processed meals into structured JSON output.
    """

    safe = []
    excluded = []

    for meal in meals:
        if meal.get("status") == "SAFE":
            safe.append(meal)
        else:
            excluded.append(meal)

    return {
        "safe_options": safe,
        "excluded_log": excluded
    }


def save_output(data: dict, filename="output.json"):
    """
    Saves JSON to file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
