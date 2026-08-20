# Session Handoff — August 20, 2026

## Where We Left Off

We are building the Home Chef Safe Menu project.

Repository:

C:\Users\jschw\GitHub\home-chef-safe-menu\repo

Python:

Python 3.14.6

The project's virtual environment is:

repo\.venv

It contains the project's existing dependencies plus Playwright.

## Important: Virtual Environment

The correct environment for this project is:

repo\.venv

When working on the project, PowerShell should show:

(.venv)

The project currently has another `.venv` at the parent level:

C:\Users\jschw\GitHub\home-chef-safe-menu\.venv

Do not use that one for this project.

The `homechef` folder is also a separate virtual environment and is not the project's environment.

## What Worked Tonight

From:

C:\Users\jschw\GitHub\home-chef-safe-menu\repo

this works:

    .\.venv\Scripts\Activate.ps1

Then:

    python --version

returns:

    Python 3.14.6

The project dependencies are installed in this environment.

Installed relevant packages include:

- beautifulsoup4
- requests
- playwright

Playwright was installed successfully.

Playwright's Chromium browser was installed successfully with:

    python -m playwright install chromium

Do NOT install the unrelated Python package named `chromium`.

## Existing Project

Repository structure currently includes:

    data/
    src/
    tests/
    main.py
    README.md
    requirements.txt
    run.ps1

Existing source files:

    src/parser.py
    src/rules.py
    src/output.py
    src/debug_html.py

The existing parser was originally designed around saved HTML.

Running the old HTML parser produced 58 "meal blocks", but some were clearly unrelated page headings such as:

- Your Opt-Out Preference Signal is Honored
- Discover New Favorites
- Meal Kits

Therefore the HTML parser is not the ideal source for the real application.

## Major Discovery Tonight

While logged into Home Chef in the normal Chrome browser, Chrome DevTools Network showed structured API requests.

The important request is:

https://www.homechef.com/api/v3/menus/24-aug-2026/standard/meals

This endpoint returned structured JSON containing actual meal data.

The response contains useful fields including:

- id
- title
- subtitle
- description
- meal label / tier
- prep time
- spice level
- nutrition information
- ingredients
- ingredient names
- ingredient-level allergen information
- instructions
- meal category
- pricing
- availability information

This is much more useful for the allergy engine than scraping the rendered HTML.

## Current Menu Data

A response from the Home Chef API was copied from Chrome DevTools using:

Network request
→ Copy
→ Copy response

The response is approximately 721.9 KB.

The JSON is currently minified onto one line. That is okay.

The next task is to save/use this data as:

    data/current-menu.json

If it has not yet been saved there, do that first tomorrow.

Do not manually edit or reformat the JSON.

## Important Safety Discovery

A meal can say:

    spice_level: "Not Spicy"

while still containing ingredients that are important to the allergy screening.

For example, the Filet Mignon meal we inspected contained:

- Garlic Pepper
- Garlic Salt
- Steak Seasoning

Therefore `spice_level` cannot be used as a proxy for being pepper-free.

The actual ingredient list needs to be inspected.

This is one of the reasons the structured API data is valuable.

## Revised Architecture

The project should now move toward:

Home Chef structured JSON
        ↓
JSON parser
        ↓
Structured meal objects
        ↓
Allergy rule engine
        ↓
Safe / Borderline / Excluded
        ↓
Structured output

The existing rule engine and output system should be reused where practical.

Do not redesign the whole project.

## Immediate Next Task

Tomorrow, start by:

1. Open the repository in VSCodium.

2. Make sure the terminal is in:

    C:\Users\jschw\GitHub\home-chef-safe-menu\repo

3. Activate:

    .\.venv\Scripts\Activate.ps1

4. Confirm:

    (.venv)

appears in PowerShell.

5. Confirm:

    data/current-menu.json

exists.

6. Inspect the JSON structure.

7. Inspect the existing:

    src/parser.py
    src/rules.py
    src/output.py
    main.py

8. Add a small JSON parsing capability.

Do NOT rewrite the entire parser yet.

## First Coding Goal

Turn the Home Chef API response into a Python list of structured meal objects.

A target object might look roughly like:

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

Do not throw away useful fields prematurely.

First get the data into Python and inspect what we actually have.

## Development Style

Use small, testable changes.

For each change:

1. Inspect.
2. Change one thing.
3. Run it.
4. Look at the output.
5. Fix the specific problem.
6. Run again.
7. Commit.

Do not replace large portions of the project unless there is a specific reason.

Suggested first commit after the JSON parser works:

    feat: parse Home Chef meal JSON

## Playwright Status

Playwright is installed and working.

Chromium successfully downloaded through Playwright.

However, Home Chef's automated browser session encountered a Cloudflare security verification page.

The normal Chrome browser was able to reach Home Chef and log in.

Therefore:

Playwright/browser automation is NOT the immediate task.

First prove that the API JSON → parser → rules pipeline works.

Later we can determine how to reliably obtain fresh menu JSON.

## Important Architectural Correction

The old plan said:

"the parser doesn't change. Only the input changes."

That assumption is no longer valid.

The HTML parser and JSON parser are different input formats.

The goal is NOT to preserve the old parser at all costs.

The goal is to preserve the useful rule engine/output architecture while using the best available Home Chef data source.

## Do Not Do Tomorrow

Do not:

- rebuild the whole application
- rewrite all existing files
- immediately solve Cloudflare
- build a dashboard
- add GitHub Actions
- add Discord/email
- optimize the system prematurely

First prove:

    current-menu.json
        ↓
    Python parser
        ↓
    meal objects
        ↓
    existing rules

Then continue one small step at a time.

## End State Tonight

The most important discovery is that Home Chef is already sending the browser structured meal data containing the ingredient information needed for the project.

We do not need to solve website scraping before we can make progress on the actual allergy-screening engine.
