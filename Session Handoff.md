# Session Handoff — August 26, 2026

## Where We Left Off

We are building the Home Chef Safe Menu project.

Repository:

C:\Users\jschw\GitHub\home-chef-safe-menu\repo

Python:

Python 3.14.6

The project's virtual environment is:

repo\.venv

The correct environment for this project is the repository-level `.venv`.

When working on the project, PowerShell should show:

    (.venv)

Do not use the parent-level environment:

C:\Users\jschw\GitHub\home-chef-safe-menu\.venv

The `homechef` environment is also separate and is not the project's environment.

---

## Current Repository State

The repository currently contains:

    data/
    src/
    tests/
    main.py
    README.md
    requirements.txt
    run.ps1
    Session Handoff.md

Current source files include:

    src/parser.py
    src/rules.py
    src/output.py
    src/debug_html.py

The repository also currently contains:

    data/31-aug-2026.json
    tests/fixtures/
    tests/test_parser.py

`README.md` and `src/parser.py` have been modified.

Parser tests and fixtures have been added.

---

## Major Discovery

Home Chef's logged-in website exposes structured menu data through an API request.

The important endpoint pattern is:

    https://www.homechef.com/api/v3/menus/{date}/standard/meals

Example:

    https://www.homechef.com/api/v3/menus/24-aug-2026/standard/meals

The response contains structured meal information including fields such as:

- id
- title
- subtitle
- description
- meal tier/category
- prep time
- spice level
- nutrition information
- ingredients
- ingredient names
- ingredient-level allergen information
- instructions
- availability
- pricing

This structured data is substantially more useful for the allergy-screening engine than scraping rendered HTML.

---

## Current Menu Data

A dated Home Chef menu response has been saved as:

    data/31-aug-2026.json

This provides a real captured menu fixture/data source for parser development.

Do not manually edit the captured Home Chef API response unless there is a specific reason to do so.

The captured response represents a particular week's menu and may become outdated.

---

## Parser Progress

The project has moved from the original HTML-scraping approach toward structured JSON parsing.

`src/parser.py` has been modified to support the structured Home Chef menu data.

Parser tests have also been added:

    tests/test_parser.py

Test fixtures are stored under:

    tests/fixtures/

The immediate objective is to reliably convert Home Chef's structured JSON into normalized meal objects while preserving useful source information.

Do not throw away useful fields prematurely.

---

## Important Safety Discovery

A meal's displayed spice level cannot be treated as evidence that the meal is safe.

For example, a meal may contain:

    spice_level: "Not Spicy"

while its ingredient list contains:

- Garlic Pepper
- Garlic Salt
- Steak Seasoning

Therefore the allergy-screening engine must inspect actual ingredient data.

Ingredient-level evidence takes priority over:

- meal names
- marketing descriptions
- spice-level labels
- assumptions about whether an ingredient "should" contain pepper

Conservative filtering is intentional.

---

## Revised Architecture

The intended architecture is:

    Home Chef structured JSON
            ↓
    JSON parser
            ↓
    Structured meal objects
            ↓
    Allergy rule engine
            ↓
    SAFE / BORDERLINE / NOT SAFE
            ↓
    Structured JSON output

The useful existing rule and output architecture should be preserved where practical.

The old HTML parser does not need to remain the primary input path.

---

## Existing HTML Parser

The original parser was designed around saved Home Chef HTML.

It previously produced approximately 58 "meal blocks", but some blocks were unrelated page content such as:

- Your Opt-Out Preference Signal is Honored
- Discover New Favorites
- Meal Kits

This demonstrated that rendered HTML is not a reliable primary data source for the application.

The HTML-related code can remain for debugging or historical purposes, but it should not drive the main structured-menu workflow unless there is a specific reason.

---

## Target Meal Object

The normalized meal representation should preserve useful information.

A simplified target may resemble:

    {
        "name": "Filet Mignon with Roasted Garlic-Chive Butter",
        "subtitle": "and loaded veggie twice-baked potato",
        "tier": "Culinary Collection",
        "prep_time": "50-60",
        "spice_level": "Not Spicy",
        "ingredients": [
            "Russet Potatoes",
            "Filets Mignon",
            "Broccoli Florets",
            "Light Sour Cream",
            "Butter",
            "Shredded Cheddar Cheese",
            "Chive Sprigs",
            "Garlic Cloves",
            "Garlic Pepper",
            "Garlic Salt",
            "Steak Seasoning"
        ]
    }

The exact structure should follow the actual API response rather than forcing the data into an unnecessarily restrictive schema.

---

## Allergy Rules

The intended screening system includes conservative exclusion/review rules for:

### Pepper and Chili Family

Examples include:

- black pepper
- white pepper
- paprika
- chili
- chile
- jalapeño
- chipotle
- serrano
- ancho
- related pepper/chili ingredients

### Bell Peppers

Bell peppers should be excluded regardless of:

- color
- preparation
- whether fresh, roasted, blended, or cooked

### Sauce Systems

Examples include:

- BBQ sauce
- pesto
- chimichurri
- harissa
- katsu sauce
- marinara when its ingredients are not sufficiently transparent

### Hidden Flavor Systems

Ingredients or ingredient systems such as:

- spices
- natural flavors
- undefined seasoning blends
- undefined sauce or marinade components

may require exclusion or additional review.

### Hard Blocks

Home Chef Cream Sauce Base or equivalent products are hard exclusions.

---

## Current Development Milestone

The project has progressed beyond simply discovering the Home Chef API.

The current milestone is:

    Connect and validate structured JSON parsing
    with the existing allergy rule engine.

The desired pipeline is:

    data/31-aug-2026.json
            ↓
        JSON parser
            ↓
    normalized meal objects
            ↓
      allergy rules
            ↓
    SAFE / BORDERLINE / NOT SAFE
            ↓
      structured output

Parser tests now exist.

The rule engine still needs to be validated against the structured meal objects before this milestone can be considered complete.

---

## Git Status

The previous README.md merge conflict has been resolved.

The local branch was successfully reconciled with the remote repository.

The repository should be checked with:

    git status

before beginning the next development session.

If there are no unexpected changes, continue with the structured JSON parser/rule-engine work.

Do not use `git push --force` unless there is a deliberate decision to rewrite remote branch history.

---

## README Status

The README has been substantially expanded and now documents:

- project purpose
- current architecture
- structured Home Chef API discovery
- safety principles
- exclusion rules
- output format
- meal object format
- repository structure
- development status
- development workflow
- Playwright status
- planned development
- technology stack
- local usage
- safety notes
- license

The README is therefore functioning as the project documentation.

The current Git conflict must be resolved before its final merged state can be considered authoritative.

Do not keep adding documentation merely for completeness.

---

## Screenshot / Meal Plan Work

A separate workflow has been established for extracting selected Home Chef meals from screenshots or captured page content.

The intended rules for that workflow are:

- Extract visible entrée meal names.
- Group meals by Home Chef delivery date.
- Exclude desserts, breakfasts, sides, snacks, and add-ons unless explicitly requested.
- Preserve meal wording as closely as possible.
- Do not invent obscured meal names.
- Use `Uncertain Meal Name` when the name cannot be reliably determined.
- Use the exact cook time shown.
- Identify effort as Easy or Standard.
- EXPRESS → Easy.
- OVEN-READY → Easy.
- Otherwise → Standard.
- Premium pricing does not determine effort.
- Identify visible cooking style when available.
- Do not assign delivery meals to weekdays unless specifically requested.

This screenshot workflow is useful for meal planning but should remain separate from the core JSON parser/rule-engine milestone unless it becomes necessary to integrate them.

---

## Playwright Status

Playwright is installed and working.

Chromium was installed successfully using:

    python -m playwright install chromium

Do NOT install the unrelated Python package named `chromium`.

Home Chef's automated browser session encountered Cloudflare security verification.

The normal Chrome browser was able to reach Home Chef and log in.

Therefore browser automation is not currently the primary development task.

The structured JSON workflow should be proven first.

---

## Development Style

Continue using small, testable changes.

For each change:

1. Inspect.
2. Change one thing.
3. Run it.
4. Inspect the result.
5. Fix the specific problem.
6. Run again.
7. Commit the working change.

Avoid replacing large portions of the project without a specific reason.

Do not redesign the whole application simply because additional improvements are possible.

---

## Immediate Next Action

The Git merge conflict has already been resolved.

Start the next session by:

1. Open the repository in VSCodium.
2. Confirm the terminal is in:

       C:\Users\jschw\GitHub\home-chef-safe-menu\repo

3. Activate:

       .\.venv\Scripts\Activate.ps1

4. Confirm:

       (.venv)

   appears in PowerShell.

5. Run:

       git status

6. Run the test suite:

       python -m pytest

7. Inspect the current parser and test results.

If the repository is clean and the tests pass, continue with the actual development milestone:

    structured Home Chef JSON
            ↓
        JSON parser
            ↓
      meal objects
            ↓
      allergy rule engine
            ↓
    SAFE / BORDERLINE / NOT SAFE

Do not reopen the resolved Git merge conflict.

---

## Do Not Do

Do not:

- rewrite the entire application
- discard the structured API approach
- immediately solve Cloudflare
- build a dashboard
- add GitHub Actions
- add Discord/email notifications
- optimize prematurely
- create duplicate sources of truth
- turn the handoff into a daily journal
- add documentation that does not improve practical use

---

## End State

The project has successfully moved past the initial HTML-scraping investigation.

The important architectural discovery is confirmed:

Home Chef provides structured menu data containing the ingredient information needed for the allergy-screening workflow.

The project now has:

- a captured dated menu JSON file
- a structured JSON parsing direction
- parser tests and fixtures
- an existing rule engine
- an existing output system
- documented exclusion rules
- a documented safety philosophy

The immediate technical issue is the unresolved Git merge conflict in `README.md`.

Once that is resolved and the tests pass, development can continue with connecting the normalized parser output to the existing allergy rule engine.