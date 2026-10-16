"""Screen a menu JSON file with the guest-allergen gate."""
import argparse
import json

from src.rules import find_guest_allergens


def load_meals(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # Accept either {"meals": [...]} or a bare list of meals.
    return data["meals"] if isinstance(data, dict) else data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument(
        "--passed",
        action="store_true",
        help="list meals that did NOT trip the allergen gate",
    )
    args = parser.parse_args()

    meals = load_meals(args.path)
    flagged = [m for m in meals if find_guest_allergens(m)]
    passed = [m for m in meals if not find_guest_allergens(m)]

    if args.passed:
        for m in passed:
            print(f"{m.get('id')}  {m.get('name')}  ({m.get('tier')}, {m.get('servings')} servings)")
        print(f"\n{len(passed)} of {len(meals)} meals passed the allergen gate")
        print("Passing means no allergen text matched. It does not mean safe.")
    else:
        for m in flagged:
            findings = find_guest_allergens(m)
            kinds = sorted({f["allergen_type"] for f in findings})
            print(f"EXCLUDE  {m.get('id')}  {m.get('name')}  {kinds}")
            for f in findings:
                print(f"           matched '{f['matched']}' in: {f['evidence'][:70]}")
        print(f"\n{len(flagged)} of {len(meals)} meals flagged")


if __name__ == "__main__":
    main()