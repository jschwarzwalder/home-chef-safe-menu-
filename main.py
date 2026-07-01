from src.parser import parse_menu
from src.rules import evaluate_meals
from src.output import build_output_json


def main():
    print("Home Chef Allergy Engine starting...")

    # Load menu from file (clean production-style input)
    with open("data/menu.txt", "r", encoding="utf-8") as f:
        raw_menu = f.read()

    meals = parse_menu(raw_menu)
    evaluated = evaluate_meals(meals)
    output = build_output_json(evaluated)

    print(output)


if __name__ == "__main__":
    main()