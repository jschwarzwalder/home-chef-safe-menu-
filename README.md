# Home Chef Allergy Screening Engine

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Status](https://img.shields.io/badge/status-active-green)
![License](https://img.shields.io/badge/license-MIT-blue)

A Python-based meal filtering and analysis tool that processes Home Chef weekly menus and identifies potentially safe meal options based on strict ingredient-level exclusion rules.

This project is designed to reduce time spent manually reviewing meal kits and to help reliably filter out unsafe ingredients such as peppers, sauces, and hidden seasoning systems.

---

## Project Status

This project is **actively developed and used for personal dietary filtering workflows**.

It is iteratively updated as new ingredient patterns, menu structures, and edge cases are discovered during real-world use.

Current development is focused on:

- parsing Home Chef's structured menu data
- preserving ingredient-level information
- refining exclusion rule logic
- improving automation of weekly menu retrieval

---

## Why this exists

Meal kit services like Home Chef often present ingredients in ways that are inconsistent, incomplete, or hidden inside sauces and seasoning systems.

For individuals with non-standard or highly sensitive allergies, this creates a high-risk and time-consuming manual review process.

This project exists to:

- Reduce manual ingredient inspection time
- Improve confidence in weekly meal selection
- Systematically eliminate unsafe ingredient exposure
- Bring structure and repeatability to an otherwise inconsistent decision process

## Goal

Home Chef menus are large, inconsistent, and often include hidden ingredients that make safe selection difficult.

This tool:

- Parses full weekly menu data (not just selected meals)
- Preserves structured meal and ingredient information
- Applies strict ingredient-level filtering rules
- Filters potentially unsafe meals automatically
- Produces structured JSON output for downstream use
- Helps identify safer alternatives across the full menu

---

## Current Architecture

The project originally began as an HTML-scraping experiment using BeautifulSoup.

During development, a more useful data source was discovered: Home Chef's own structured API response used by the logged-in calendar page.

A current menu request has the form:

`https://www.homechef.com/api/v3/menus/{date}/standard/meals`

For example:

`https://www.homechef.com/api/v3/menus/24-aug-2026/standard/meals`

The API response contains structured meal objects with information including:

- Meal title
- Subtitle
- Description
- Meal tier/category
- Prep time
- Spice level
- Nutrition information
- Ingredients
- Ingredient names
- Ingredient-level allergen information
- Instructions
- Availability
- Pricing

This structured data is substantially more useful for allergy screening than attempting to infer meal information from rendered HTML.

---

## Quick Start

1. Install dependencies:
   pip install -r requirements.txt

2. Run the main script:
   python main.py


3. Provide or load weekly Home Chef menu data

4. Review generated output:
   - safe_options
   - borderline meals
   - excluded meals
 
---

## Important Safety Principle

A meal's displayed spice level is **not sufficient** to determine whether it is safe.

For example, a meal may be labeled:

`spice_level: "Not Spicy"`

while its ingredient list contains:

- Garlic Pepper
- Garlic Salt
- Steak Seasoning

Therefore the screening engine must inspect the actual ingredient data.

The project prioritizes ingredient-level evidence over assumptions based on meal names, marketing labels, or spice-level indicators.

---

## Current Architecture

The project originally began as an HTML-scraping experiment using BeautifulSoup.

During development, a more useful data source was discovered: Home Chef's own structured API response used by the logged-in calendar page.

A current menu request has the form:

`https://www.homechef.com/api/v3/menus/{date}/standard/meals`

For example:

`https://www.homechef.com/api/v3/menus/24-aug-2026/standard/meals`

The API response contains structured meal objects with information including:

- Meal title
- Subtitle
- Description
- Meal tier/category
- Prep time
- Spice level
- Nutrition information
- Ingredients
- Ingredient names
- Ingredient-level allergen information
- Instructions
- Availability
- Pricing

This structured data is substantially more useful for allergy screening than attempting to infer meal information from rendered HTML.

---

## Quick Start

1. Install dependencies:
   pip install -r requirements.txt

2. Run the main script:
   python main.py

3. Provide or load weekly Home Chef menu data

4. Review generated output:
   - safe_options
   - borderline meals
   - excluded meals
 
---

## Important Safety Principle

A meal's displayed spice level is **not sufficient** to determine whether it is safe.

For example, a meal may be labeled:

`spice_level: "Not Spicy"`

while its ingredient list contains:

- Garlic Pepper
- Garlic Salt
- Steak Seasoning

Therefore the screening engine must inspect the actual ingredient data.

The project prioritizes ingredient-level evidence over assumptions based on meal names, marketing labels, or spice-level indicators.

---
## Core Features

- Full menu ingestion from structured Home Chef menu data
- Entrée-only filtering (excludes sides, desserts, add-ons, etc.)
- Ingredient-level filtering
- Strict exclusion engine including:
  - Pepper and chili family (black pepper, paprika, jalapeño, etc.)
  - Bell peppers in any form or color
  - Sauce systems (pesto, BBQ, chimichurri, harissa, etc.)
  - Cream Sauce Base products
  - Undefined seasoning systems such as "spices" or "natural flavors"
- Tier-aware ranking system:
  - Standard meals (preferred)
  - Culinary Collection
  - Premium meals (last resort only)
- JSON-first output format for automation and analysis

---

## Output Format

The intended output structure is:

{
  "safe_options": [],
  "selected_order_review": [],
  "better_alternatives": [],
  "borderline": [],
  "excluded_log": []
}

---

## Meal Object Format

Example safe meal:

{
  "name": "Filet Mignon with Roasted Garlic-Chive Butter",
  "subtitle": "and loaded veggie twice-baked potato",
  "ingredients": [
    {
      "name": "Russet Potatoes",
      "amount": 2,
      "allergens": []
    },
    {
      "name": "Light Sour Cream",
      "amount": "4 oz.",
      "allergens": ["milk"]
    },
    {
      "name": "Butter",
      "amount": "2 oz.",
      "allergens": ["milk"]
    }
  ],
  "allergen_tags": ["milk"]
}

Example excluded meal:

{
  "name": "Smoky Peppercorn Beef Burger",
  "ingredients": [
    {
      "name": "Ground Beef",
      "amount": "10 oz.",
      "allergens": [],
      "photo": null
    },
    {
      "name": "Butter",
      "amount": "2 oz.",
      "allergens": ["milk"],
      "photo": null
    },
    {
      "name": "Garlic Pepper",
      "amount": "1 tsp.",
      "allergens": [],
      "photo": null
    }
  ],
  "allergen_tags": ["milk"]
}


---

## Exclusion Rules

The intended rule system identifies ingredients and ingredient systems that require exclusion or additional review.

### Pepper and chili family
black pepper, white pepper, paprika, chili, chile, jalapeño, chipotle, serrano, ancho, etc.

### Bell peppers
Any color or preparation (fresh, roasted, blended, or cooked)

### Sauce systems
BBQ sauce, pesto (any type), chimichurri, harissa, katsu sauce, marinara (if not fully transparent)

### Hidden flavor systems
"spices", "natural flavors", or undefined seasoning blends within sauces or marinades

### Hard blocks
Home Chef Cream Sauce Base or equivalent products

---

## Design Philosophy

This system prioritizes:

- Ingredient-level accuracy over assumptions
- Conservative filtering (avoid false negatives)
- Full menu awareness rather than partial evaluation
- Structured machine-readable JSON output

---

## Planned Enhancements

- Connect parsed meals to the exclusion engine
- Generate safe/borderline/excluded output
- Improve automated retrieval of fresh weekly menu data
- AnyList integration

---

## Repository Structure

Current project structure:

    home-chef-safe-menu/
    │
    └── repo/
        ├── data/
        │   ├── current-menu.json
        │   └── saved menu data
        │
        ├── src/
        │   ├── parser.py
        │   ├── rules.py
        │   ├── output.py
        │   └── debug_html.py
        │
        ├── tests/
        ├── main.py
        ├── run.ps1
        ├── requirements.txt
        ├── README.md
        └── Session Handoff.md

`Session Handoff.md` is a development continuity note and records where the project was left during active development.

---


## Development Status

### Completed

- Git repository established
- Python virtual environment established
- Playwright installed
- Saved Home Chef HTML successfully processed
- Initial HTML parser developed
- Home Chef structured menu data discovered
- Structured meal JSON successfully obtained
- Ingredient-level data confirmed to be available
- Structured JSON parser implemented
- Parser tests added
- Rule tests added

### Current Milestone

Connect the structured meal parser to the allergy rule engine.

Current pipeline:

    Home Chef structured JSON
        │
        ▼
    JSON Parser
        │
        ▼
    Structured Meal Objects
        │
        ▼
    Allergy Rule Engine
        │
        ├── SAFE
        ├── BORDERLINE
        └── NOT SAFE
        │
        ▼
    Structured JSON Output

---

## Development Workflow

Development should proceed through small, testable changes.

Preferred workflow:

1. Inspect the existing code.
2. Make one small change.
3. Run the program.
4. Inspect the result.
5. Fix the specific problem revealed.
6. Run again.
7. Commit the working change.
8. Move to the next milestone.

Avoid replacing large portions of the project unless there is a specific reason.

Suggested milestone commits include:

    feat: parse Home Chef meal JSON

    feat: apply allergy rules to structured meal data

    feat: generate structured recommendation output

This makes it easier to identify and undo changes when something goes wrong.

---

## Browser Automation

Playwright is installed and available for future browser automation.

However, browser automation is **not currently the primary development task**.

A Playwright browser session encountered Home Chef's Cloudflare security verification, while the normal Chrome browser was able to reach the site and log in.

The immediate goal is therefore to make the screening engine work with captured structured menu data before solving automated browser access.

Future automation may eventually use Playwright or another appropriate approach to obtain fresh menu data.

---

## Planned Development

### Phase 1 — Structured Menu Processing

- Parse Home Chef API JSON
- Create normalized meal objects
- Preserve ingredient-level information
- Connect the existing rule engine
- Generate safe/borderline/excluded results

### Phase 2 — Order Review

Identify meals already selected in the user's Home Chef order and review them separately from the general menu.

### Phase 3 — Detailed Ingredient Review

Use the first-pass rules to reduce the full menu to a smaller candidate set.

For example:

    Full weekly menu
          ↓
    First-pass screening
          ↓
    Small candidate list
          ↓
    Detailed ingredient review
          ↓
    Final classification

This prevents expensive or complicated analysis from being performed on every meal unnecessarily.

### Phase 4 — Automated Menu Acquisition

Determine the most reliable way to obtain fresh Home Chef menu data automatically.

Possible technologies include:

- Playwright
- Home Chef API requests
- Other browser/network automation

The implementation should be based on what proves reliable rather than committing prematurely to one scraping method.

---

## Tech Stack

- Python 3.11+
- Tested with Python 3.14.6
- JSON-based processing pipeline
- requests
- BeautifulSoup
- Playwright
- pytest

---

## Local Usage

Install dependencies:

    python -m pip install -r requirements.txt

Run the application:

    python main.py

Run the test suite:

    python -m pytest

---

## Notes

- This project is intended for personal dietary filtering and meal-selection assistance.
- It is a screening tool and should not be treated as a guarantee of dietary safety.
- Menu data may change between weeks.
- Home Chef may change its website, API structure, ingredient data, or security mechanisms.
- Conservative filtering is intentional.
- The system should prefer identifying a meal as requiring review rather than making an unsupported assumption that it is safe.
- Captured menu data represents a specific week's menu and may become outdated.
---

## License

MIT License
