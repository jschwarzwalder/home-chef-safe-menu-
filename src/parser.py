"""
Parses raw Home Chef menu text into structured meal objects.
"""

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
