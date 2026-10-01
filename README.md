 # Home Chef Allergy Screening Engine

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Status](https://img.shields.io/badge/status-active-green)
![License](https://img.shields.io/badge/license-MIT-blue)

A Python-based meal filtering and analysis tool that processes Home Chef weekly menus and identifies potentially safe meal options based on strict ingredient-level exclusion rules.

This project is designed to reduce time spent manually reviewing meal kits and to help reliably filter out unsafe ingredients such as peppers, sauces, and hidden seasoning systems.

The system currently focuses on obtaining structured Home Chef JSON data, reducing that data into a compact meal representation, and preparing the resulting meals for ingredient-level screening.
---

 ## Project Status

 This project is **actively developed and used for personal dietary filtering workflows**.

 The current development pipeline has progressed beyond the original HTML-scraping approach. The project now works primarily with Home Chef's structured JSON menu data and includes a menu-cleaning utility that reduces the large API response into a smaller, machine-readable representation.

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

```
https://www.homechef.com/api/v3/menus/{date}/standard/meals
```

 For example:

`https://www.homechef.com/api/v3/menus/24-aug-2026/standard/meals`

The API response contains structured meal objects with information including:

 Depending on the response, the menu data can contain information such as:

 - Meal ID
- Meal title
- Meal subtitle
- Meal description
- Meal category
- Meal tier
- Serving information
- Prep time
- Spice level
- Nutrition information
- Ingredients
- Ingredient names
- Ingredient-level allergen information
- Instructions
- Availability
- Pricing
- Recipe information

This structured data is substantially more useful for allergy screening than attempting to infer meal information from rendered HTML.

 ## Current JSON Acquisition Workflow

 Home Chef requires authentication for some menu/API access.

 The current workflow therefore uses an authenticated browser to obtain the weekly JSON rather than attempting to bypass authentication or security protections.

 The current process is:

```
Generate weekly URL
        ↓
Open URL in authenticated browser
        ↓
Obtain Home Chef JSON
        ↓
Save JSON in data/
        ↓
Run clean_menu.py
        ↓
Generate compact menu
        ↓
Run screening
```

 The project does **not** currently attempt to bypass Home Chef authentication or Cloudflare protections.

---

 # Home Chef Menu URL Generator

 The project includes a utility for generating weekly Home Chef menu API URLs.

 The utility is located at:

```
tools/homechef_urls.py
```

 It calculates Monday dates and generates the corresponding Home Chef menu URLs.

 The utility does **not** log in to Home Chef or download menu data.

 ## Basic Usage

 From the repository root:

```
python tools/homechef_urls.py
```

 With no date supplied, the tool finds the next Monday and generates one URL.

 Example:

```
Starting Monday: 14-sep-2026
Weeks: 1

14-sep-2026
https://www.homechef.com/api/v3/menus/14-sep-2026/standard/meals
```

 ## Generate Multiple Weeks

 Use `--weeks` to generate several consecutive weekly URLs:

```
python tools/homechef_urls.py --weeks 5
```

 This generates five consecutive Mondays.

 ## Start From a Specific Date

 A date can be supplied in `DD-mon-YYYY` format:

`https://www.homechef.com/api/v3/menus/{date}/standard/meals`

If the supplied date is not a Monday, the utility advances to the next Monday.

 For example:

```
16-sep-2026 → 21-sep-2026
```

 Multiple weeks can also be generated:

```
python tools/homechef_urls.py 16-sep-2026 --weeks 5
```

 ## Supplying a Monday

 If the supplied date is already a Monday, it is used as the starting date:

```
python tools/homechef_urls.py 21-sep-2026 --weeks 3
```

 This produces:

```
21-sep-2026
28-sep-2026
05-oct-2026
```

 ## URL Generator Tests

 The URL generator has its own test suite:

```
tests/test_homechef_urls.py
```

 The tests cover:

 - Monday date handling
- Finding the next Monday
- Multiple weekly dates
- Seven-day intervals
- Date formatting
- Home Chef URL formatting
- Invalid dates
- Invalid date formats
- Invalid week counts
- URL generation from arbitrary starting dates

 Run the complete test suite with:

```
python -m pytest
```

---

 # Menu Cleaning

 The project now includes a dedicated menu-cleaning utility:

```
src/clean_menu.py
```

 Its purpose is to take the large Home Chef menu JSON response and produce a much smaller representation containing only information needed for programmatic screening.

 Run it with:

```
python src/clean_menu.py data/14-sep-2026.json
```

 This creates:

```
data/14-sep-2026-clean.json
data/14-sep-2026-scan.txt
```

 The JSON file is intended for programmatic processing.

 The text file is a compact, human-readable representation useful for inspection and manual review.

---

 # What `clean_menu.py` Does

 The cleaner currently keeps:

 - Meal ID
- Meal name
- Meal type
- Meal tier
- Serving amount
- Ingredient names
- Recipe URL when available

 It intentionally removes large amounts of API metadata that are not required for the first-stage screening process.

 The cleaner intentionally omits:

 - Ingredient amounts
- Home Chef allergen flags
- Instructions
- Images
- Nutrition information
- Descriptions
- Other large API metadata

 This keeps the resulting files significantly smaller and easier to process.

---

 # Meal Category Filtering

 The cleaner removes meal categories that are outside the current screening workflow.

 The excluded categories include:

```
Premium?  [tier is preserved; see Tier Handling below]
Breakfast
Heat & Eat
Dessert
Snack
Side
Mix & Match
Protein
Protein Pack
```

 The important distinction is that **meal type and meal tier are separate concepts**.

 The cleaner removes unwanted meal _types_, while preserving the meal's _tier_ so that Standard, Culinary Collection, and Premium meals can remain distinguishable later in the pipeline.

---

 # Tier Handling

 Home Chef meals may have different tiers, including:

 - Standard
- Culinary Collection
- Premium

 The current cleaning stage does **not** treat Premium or Culinary Collection as an automatic ingredient exclusion.

 Instead, the tier is preserved in the cleaned meal object:

```
{
  "name": "Example Meal",
  "type": "Entrée",
  "tier": "Premium",
  "servings": 2,
  "ingredients": []
}
```

 This allows later screening and ordering logic to make use of the tier information without losing meals prematurely.

 Tier handling and allergy screening are therefore separate stages.

---

 # Serving Size Handling

 The cleaner supports both 2-serving and 4-serving workflows.

 The command-line option is:

```
--amount
```

 The available values are:

```
2
4
```

 ## Two-Serving Workflow

 The default is 2 servings:

```
python src/clean_menu.py data/14-sep-2026.json
```

 This produces the 2-serving meal set.

 ## Four-Serving Workflow

 Use:

```
python src/clean_menu.py data/14-sep-2026.json --amount 4
```

 When requesting 4 servings, the desired behavior is to retain:

 - 2-serving meals
- 4-serving meals

 A 2-serving meal should **not** be discarded simply because the requested amount is 4.

 The serving amount should therefore be interpreted as a maximum acceptable meal size for the current workflow rather than an exact equality requirement.

 Family meals are treated as 4-serving meals.

---

 # Detailed Ingredient Retrieval

 The initial weekly menu response does not always contain all of the detailed ingredient information required for comprehensive screening.

 `clean_menu.py` can therefore request additional information for individual meals using the Home Chef nutritional-facts endpoint:

```
https://www.homechef.com/api/v3/nutritional_facts/{meal_id}
```

 The detailed response can contain ingredient names with additional ingredient information, including parenthetical ingredient lists.

 This is important because an ingredient that appears harmless at the top level may contain additional ingredients that need to be screened.

 The cleaner therefore follows this process:

```
Meal from weekly JSON
        ↓
Get Meal ID
        ↓
Request detailed nutritional facts
        ↓
Extract detailed ingredients
        ↓
Use detailed ingredients when available
        ↓
Fall back to original menu ingredients if necessary
```

 If the detailed request fails, the cleaner falls back to the ingredient names already present in the original menu data.

 This allows processing to continue even when an individual detailed API request is unavailable.

---

 # Cleaned JSON Format

 The output file has the general structure:

```
{
  "meals": [
    {
      "id": "12345",
      "name": "Example Meal",
      "type": "Entrée",
      "tier": "Standard",
      "servings": 2,
      "ingredients": [
        "Ground Beef",
        "Russet Potatoes",
        "Butter"
      ],
      "recipe_url": "..."
    }
  ]
}
```

 The `recipe_url` field is preserved when Home Chef provides one.

 This will be useful for future browser and ordering workflows.

---

 # Scan Text Output

 In addition to JSON, the cleaner creates a compact text file:

```
data/14-sep-2026-scan.txt
```

 The format is designed to make the meal list easy to inspect.

 Example:

```
Filet Mignon with Roasted Garlic-Chive Butter | Entrée | Standard
Russet Potatoes; Light Sour Cream; Butter; Garlic; Chives

Chicken with Roasted Vegetables | Entrée | Culinary Collection
Chicken Breast; Carrots; Potatoes; Olive Oil
```

 This format removes unnecessary API metadata while retaining the information needed for first-pass ingredient screening.

---

 # Ingredient Screening Rules

 The current rule engine is located at:

```
src/rules.py
```

 The rules are ingredient-based rather than relying on meal names or marketing labels.

 The current rule groups include:

 ## Pepper and Chili Family

 Examples include:

```
black pepper
white pepper
paprika
chili
chile
jalapeño
chipotle
serrano
ancho
```

 ## Bell Peppers

 The current rule explicitly identifies:

```
bell pepper
```

 This is intended to cover bell peppers regardless of color or preparation when the ingredient text contains the relevant term.

 ## Sauce Systems

 Current blocked sauce systems include:

```
pesto
bbq sauce
chimichurri
harissa
katsu sauce
marinara
```

 These are treated conservatively because prepared sauces can contain additional ingredients that are not obvious from the meal's primary ingredient name.

 ## Hard Blocks

 The current hard-block list includes:

```
cream sauce base
```

---

 # Rule Engine

 The current low-level rule function is:

```
is_excluded(text)
```

 It performs a case-insensitive ingredient text search against the configured exclusion terms.

 Conceptually:

```
Ingredient
    ↓
Normalize text
    ↓
Check exclusion terms
    ↓
Match?
 ┌──┴──┐
Yes    No
 ↓      ↓
Block  Continue
```

 The rule engine is intentionally conservative.

 A match should result in exclusion or additional review rather than an assumption that the ingredient is acceptable.

---

 # Current Screening Status

 The project currently has the basic rule definitions in place, but the full classification pipeline is still under active development.

 The current `evaluate_meals()` implementation is a temporary pass-through:

```
def evaluate_meals(meals):
    return meals
```

 Therefore, the current system should **not** be described as having a completed automatic SAFE/BORDERLINE/NOT SAFE classification pipeline.

 The immediate development goal is to connect the cleaned meal data to the rule engine and produce the final classification output.

---

 # Planned Classification Pipeline

 The intended screening architecture is:

```
Cleaned Home Chef JSON
        ↓
Ingredient extraction
        ↓
Ingredient rule evaluation
        ↓
Meal classification
        │
        ├── SAFE
        ├── BORDERLINE
        └── NOT SAFE
        ↓
Structured output
```

 The distinction between the cleaner and classifier is intentional.

 `clean_menu.py` answers:

 > What meals and ingredients should we process?

 The rule/classification system answers:

 > What do those ingredients mean for the screening rules?

---

 # Output Format

 The intended final output structure is:

```
{
  "safe_options": [],
  "selected_order_review": [],
  "better_alternatives": [],
  "borderline": [],
  "excluded_log": []
}
```

 This output structure is intended to support both automated processing and human review.

 The final classification pipeline is still under development.

---

 # Order Review

 A future stage will identify meals already selected in the user's Home Chef order.

 Those meals should be reviewed separately from the general menu because an already-selected meal has a different purpose from a potential alternative.

 The intended structure is:

```
Weekly Menu
    │
    ├── General Candidate Meals
    │
    └── Already Selected Meals
              ↓
         Order Review
```

 This will allow the system to identify potential issues with an existing order while separately identifying alternatives from the broader menu.

---

 # Two-Stage Ingredient Review

 The intended system uses a first-pass screening process followed by more detailed review.

```
Full Weekly Menu
       ↓
First-Pass Ingredient Screening
       ↓
Smaller Candidate Set
       ↓
Detailed Ingredient Review
       ↓
Final Classification
```

 This prevents more expensive or complicated analysis from being performed unnecessarily on every meal.

 The first pass can eliminate obvious matches such as pepper-family ingredients or known blocked sauces.

 Borderline or ambiguous ingredients can then be examined separately.

---

 # Important Safety Principle

 A meal's displayed spice level is **not sufficient** to determine whether it should pass ingredient screening.

 For example, a meal may be labeled:

```
spice_level: "Not Spicy"
```

 while its ingredients contain:

```
Garlic Pepper
Garlic Salt
Steak Seasoning
```

 The screening engine therefore prioritizes the actual ingredient data over:

 - Meal names
- Marketing descriptions
- Spice-level labels
- General assumptions about a recipe

 Ingredient-level evidence is the primary source for screening decisions.

---

 # Repository Structure

 The current project structure is:

```
home-chef-safe-menu/
│
└── repo/
    │
    ├── data/
    │   ├── current-menu.json
    │   ├── saved menu JSON
    │   ├── *-clean.json
    │   └── *-scan.txt
    │
    ├── src/
    │   ├── parser.py
    │   ├── clean_menu.py
    │   ├── rules.py
    │   ├── classifier.py
    │   ├── output.py
    │   └── debug_html.py
    │
    ├── tools/
    │   └── homechef_urls.py
    │
    ├── tests/
    │   ├── fixtures/
    │   ├── test_clean_menu.py
    │   ├── test_homechef_urls.py
    │   ├── test_parser.py
    │   └── test_rules.py
    │
    ├── main.py
    ├── run.ps1
    ├── requirements.txt
    ├── README.md
    ├── Next Session.md
    └── Session Handoff.md
```

 `Next Session.md` and `Session Handoff.md` are development continuity documents and are not part of the runtime processing pipeline.

---

 # Development Status

 ## Completed

 - Git repository established
- Python virtual environment established
- Playwright installed
- Saved Home Chef HTML successfully processed
- Initial HTML parser developed
- Home Chef structured menu data discovered
- Structured weekly menu JSON obtained
- Ingredient-level data confirmed to be available
- Structured JSON parser implemented
- Parser tests added
- Initial ingredient exclusion rules added
- Rule tests added
- Weekly Home Chef URL generator implemented
- URL generator tests added
- Menu cleaning utility implemented
- Compact JSON output implemented
- Compact text/scan output implemented
- Meal type filtering implemented
- Meal tier preservation implemented
- Family meal serving handling implemented
- Detailed ingredient retrieval implemented
- Fallback to original menu ingredients implemented
- Recipe URL preservation implemented

 ## Current Milestone

 The current milestone is to connect the cleaned menu pipeline to the practical allergy-screening and classification rules.

 Current pipeline:

```
Home Chef Weekly JSON
        │
        ▼
    clean_menu.py
        │
        ├── Filter meal types
        ├── Determine serving size
        ├── Preserve tier
        ├── Retrieve detailed ingredients
        └── Normalize meal objects
        │
        ▼
   Cleaned Menu JSON
        │
        ▼
   Allergy Rule Engine
        │
        ├── SAFE
        ├── BORDERLINE
        └── NOT SAFE
        │
        ▼
 Structured Output
```

---

 # Development Workflow

 Development should proceed through small, testable changes.

 Preferred workflow:

 1. Inspect the existing code.
2. Make one small change.
3. Run the relevant tests.
4. Run the program.
5. Inspect the generated output.
6. Fix the specific problem revealed.
7. Run the tests again.
8. Commit the working change.
9. Move to the next milestone.

 Avoid replacing large portions of the project unless there is a specific reason.

 Suggested milestone commits include:

```
feat: parse Home Chef meal JSON

feat: clean Home Chef menu data

feat: retrieve detailed meal ingredients

feat: apply allergy rules to structured meal data

feat: generate structured recommendation output
```

 Small commits make it easier to identify and undo changes when something goes wrong.

---

 # Browser Automation

 Playwright is installed and available for future browser automation.

 However, browser automation is **not currently the primary development task**.

 A Playwright browser session encountered Home Chef's Cloudflare security verification, while the normal Chrome browser was able to reach the site and log in.

 The immediate priority is therefore to make the structured JSON → cleaning → screening pipeline reliable before solving fully automated browser access.

 Future automation may use:

 - Playwright
- Direct Home Chef API requests where appropriate
- Other browser/network automation

 The implementation should be based on what proves reliable rather than committing prematurely to one acquisition method.

---

 # Running the Project

 ## Install Dependencies

 From the repository root:

```
python -m pip install -r requirements.txt
```

 ## Generate Home Chef URLs

```
python tools/homechef_urls.py
```

 ## Clean a Saved Menu

```
python src/clean_menu.py data/14-sep-2026.json
```

 ## Clean for a Four-Serving Workflow

```
python src/clean_menu.py data/14-sep-2026.json --amount 4
```

 The 4-serving workflow is intended to retain both 2-serving and 4-serving meals.

 ## Run the Main Application

```
python main.py
```

 ## Run Tests

```
python -m pytest
```

---

 # Testing

 The project currently contains tests for:

 - Menu cleaning
- Home Chef URL generation
- JSON parsing
- Ingredient exclusion rules

 The primary test files are:

```
tests/test_clean_menu.py
tests/test_homechef_urls.py
tests/test_parser.py
tests/test_rules.py
```

 Run all tests with:

```
python -m pytest
```

 Tests should be run after changes to parsing, cleaning, rule logic, or output generation.

---

 # Planned Development

 ## Phase 1 — Structured Menu Processing

- Parse Home Chef API JSON
- Normalize meal objects
- Preserve ingredient-level information
- Retrieve detailed ingredient information
- Clean unwanted menu categories
- Preserve tier information
- Support 2-serving and 4-serving workflows

 ## Phase 2 — Allergy Screening

- Connect cleaned meals to the rule engine
- Apply ingredient exclusion rules
- Detect known blocked ingredients
- Detect blocked sauce systems
- Identify undefined seasoning systems
- Generate SAFE/BORDERLINE/NOT SAFE classifications

 ## Phase 3 — Automated Menu Acquisition

 Determine the most reliable way to obtain fresh Home Chef menu data automatically.

 Potential technologies include:

 - Playwright
- Home Chef API requests
- Other browser/network automation

 The project should favor reliability and maintainability over prematurely committing to a particular acquisition method.

 ## Phase 4 — AnyList Integration

 Integrate selected meals and/or ingredients with AnyList as part of the eventual meal-selection and grocery workflow.

---

 # Design Philosophy

 This project prioritizes:

 - Ingredient-level evidence over assumptions
- Conservative screening
- Full-menu awareness
- Structured machine-readable data
- Separation of data acquisition, cleaning, screening, and output
- Small, testable development changes
- Preservation of useful source information
- Human review for ambiguous cases

 The cleaner should not make allergy decisions that belong to the screening engine.

 Likewise, the screening engine should not need to understand the full complexity of the raw Home Chef API response.

 Each stage should have a focused responsibility.

---

 # Notes

 - This project is intended for personal dietary filtering and meal-selection assistance.
- It is a screening tool and should not be treated as a guarantee of dietary safety.
- Menu data may change between weeks.
- Home Chef may change its website, API structure, ingredient data, or security mechanisms.
- Captured menu data represents a specific week's menu and may become outdated.
- Conservative filtering is intentional.
- The system should prefer identifying a meal as requiring review rather than making an unsupported assumption that it is safe.
- Tier information such as Standard, Culinary Collection, and Premium is preserved independently from ingredient screening.
- A 4-serving workflow should retain both 2-serving and 4-serving meals rather than treating serving amount as an exact-match filter.
- The current classification layer remains under active development.

---

 # License

 MIT License

