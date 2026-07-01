from src.parser import extract_meals_from_text
from src.rules import evaluate_meals
from src.output import build_output_json


def main():
    print("Home Chef Allergy Engine starting...")

    # Load menu from file (clean production-style input)
    with open("data/menu.txt", "r", encoding="utf-8") as f:
        raw_menu = f.read()

    # TEMP: paste your menu text here (you can replace later with file input)
    # raw_menu_text = open("data/menu.txt", "r", encoding="utf-8").read()

    file_path = r"data/Home Chef Meal Delivery Service, Fresh Ingredients to Cook at Home _ Home Chef.html"

    with open(file_path, "r", encoding="utf-8") as f:
        raw_html = f.read()

    meals = extract_meals_from_text(raw_html)

    """ 
    print(f"\nFOUND: {len(meals)} MEAL BLOCKS\n")

    for m in meals[:10]:
        print("-----")
        print(m) 
    """


if __name__ == "__main__":
    main()