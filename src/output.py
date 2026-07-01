"""
Builds final JSON output structure.
"""

import json

import json

def build_output_json(meals):
    """
    Temporary output builder.
    Converts whatever comes in into structured JSON.
    """

    output = {
        "safe_options": meals,
        "selected_order_review": [],
        "better_alternatives": [],
        "borderline": [],
        "excluded_log": []
    }

    return json.dumps(output, indent=2)

    """
    Converts processed meals into structured JSON output.
    """

"""     safe = []
    excluded = []

    for meal in meals:
        if meal.get("status") == "SAFE":
            safe.append(meal)
        else:
            excluded.append(meal)

    return {
        "safe_options": safe,
        "excluded_log": excluded
    } """


def save_output(data: dict, filename="output.json"):
    """
    Saves JSON to file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
