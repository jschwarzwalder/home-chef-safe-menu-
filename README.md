# Home Chef Allergy Screening Engine

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Status](https://img.shields.io/badge/status-active-green)
![License](https://img.shields.io/badge/license-MIT-blue)

A Python-based meal filtering and analysis tool that processes Home Chef weekly menus and identifies safe meal options based on strict ingredient exclusion rules.

This project is designed to reduce time spent manually reviewing meal kits and to help reliably filter out unsafe ingredients such as peppers, sauces, and hidden seasoning systems.

---

## Project Status

This project is **actively developed and used for personal dietary filtering workflows**.

It is iteratively updated as new ingredient patterns, menu structures, and edge cases are discovered during real-world use.

Planned improvements are focused on:

- improving ingredient parsing accuracy
- expanding menu ingestion methods
- increasing automation of weekly meal retrieval
- refining exclusion rule logic

---

## Why this exists

Meal kit services like Home Chef often present ingredients in ways that are inconsistent, incomplete, or hidden inside sauces and seasoning systems.

For individuals with non-standard or highly sensitive allergies, this creates a high-risk and time-consuming manual review process.

This project exists to:

- Reduce manual ingredient inspection time
- Improve confidence in weekly meal selection
- Systematically eliminate unsafe ingredient exposure
- Bring structure and repeatability to an otherwise inconsistent decision process
  
---

## Goal

Home Chef menus are large, inconsistent, and often include hidden ingredients that make safe selection difficult.

This tool:

- Parses full weekly menu data (not just selected meals)
- Applies strict ingredient-level filtering rules
- Filters unsafe meals automatically
- Produces structured JSON output for downstream use
- Helps identify safer alternatives across the full menu

---

## Quick Start

1. Install dependencies:
   pip install -r requirements.txt

2. Run the main script:
   python monitor.py

3. Provide or load weekly Home Chef menu data

4. Review generated output:
   - safe_options
   - borderline meals
   - excluded meals
 
---

## Core Features

- Full menu ingestion (not limited to cart or selected meals)
- Entrée-only filtering (excludes sides, desserts, add-ons, etc.)
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

The system returns strict JSON only:

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
  "meal": "Coconut Yuzu Chicken",
  "tier": "Standard",
  "status": "SAFE",
  "ingredients": ["chicken", "rice", "carrots"],
  "reason": "No excluded ingredients detected"
}

Example excluded meal:

{
  "meal": "Smoky Peppercorn Beef Burger",
  "tier": "Culinary Collection",
  "status": "NOT SAFE",
  "reason": "Contains black pepper / peppercorn seasoning"
}

---

## Exclusion Rules

Meals are automatically excluded if they contain:

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

- Playwright-based browser scraping for logged-in menus
- Automated extraction of ingredient lists from nutrition pages
- Discord or email alert system for safe meals
- Web dashboard for filtering and selection
- Historical tracking of safe meals over time

---

## Tech Stack

- Python 3.11+
- JSON-based processing pipeline
- Planned: Playwright for browser automation
- Optional: GitHub Actions for scheduled runs

---

## Local Usage

Install dependencies:

pip install -r requirements.txt

Run the script:

python monitor.py

---

## Notes

- This project is intended for personal dietary filtering use.
- Menu data is user-provided or extracted from Home Chef pages.
- Output is optimized for structured analysis and automation rather than human-readable summaries.

---

## License

MIT License
