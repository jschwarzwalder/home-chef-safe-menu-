# Session Handoff — August 28, 2026

## Where We Left Off

We are building the **Home Chef Safe Menu** project.

Repository:

```text
C:\Users\jschw\GitHub\home-chef-safe-menu\repo
```

The authoritative long-term project description is now in:

```text
Master Project Notes
```

`README.md` remains the project-facing documentation.

This handoff is intentionally shorter than the Master Project Notes. It records **current development state and recent decisions**, not the entire project history.

---

## Current Environment

Python:

```text
Python 3.14.6
```

Project virtual environment:

```text
repo\.venv
```

Use the repository-level `.venv`.

PowerShell should show:

```text
(.venv)
```

Do not use:

```text
C:\Users\jschw\GitHub\home-chef-safe-menu\.venv
```

The separate `homechef` environment is also not the project environment.

---

## Current Repository

Primary files:

```text
src/parser.py
src/rules.py
src/output.py
src/debug_html.py
main.py
tests/
data/
requirements.txt
run.ps1
README.md
Session Handoff.md
```

Important captured data:

```text
data/31-aug-2026.json
```

Parser tests and fixtures exist under:

```text
tests/
tests/fixtures/
```

Before doing anything else next session:

```powershell
git status
python -m pytest
```

Then inspect the current parser/rule-engine state rather than rebuilding anything.

---

# Important Architectural State

The project has moved away from HTML scraping as its primary data source.

Current intended pipeline:

```text
Home Chef structured JSON
        ↓
JSON parser
        ↓
Normalized meal objects
        ↓
Practical screening
        ↓
Candidate shortlist
        ↓
Human investigation/selection
```

The captured Home Chef JSON is the important development fixture.

**Do not restart parser development unless the tests or actual data show a problem.**

The next major development work is connecting/validating the practical screening rules against the normalized parser output.

---

# Current Project Philosophy

The project is **not** trying to make an absolute medical safety determination.

It is a **practical meal-triage tool**.

The question is:

> Which meals are worth spending limited attention on, given what can realistically be removed or substituted without turning dinner into a project?

The computer should eliminate obvious time-wasters and surface useful candidates.

The human makes the final decision.

---

# Major Rule Correction From Earlier Notes

The older allergy-rule description was too conservative for the actual household workflow.

The current model is:

```text
PROBLEMATIC?
      ↓
CAN IT BE ADAPTED?
      ↓
IS THE ADAPTATION WORTH THE EFFORT?
```

Those are three separate questions.

The presence of pepper does **not** automatically mean "reject."

---

# Current Practical Screening Rules

## Bell Pepper

Bell pepper is generally removable.

```text
Bell Pepper
    ↓
remove it
    ↓
KEEP CANDIDATE
```

Do **not** automatically exclude a meal because it contains bell pepper.

---

## Standalone Garlic Pepper

Standalone Garlic Pepper is generally replaceable.

Typical household substitutions:

```text
Garlic Salt
Garlic Powder
```

Therefore:

```text
Standalone Garlic Pepper
    ↓
ADAPTABLE
```

Keep the meal as a candidate.

---

## Pepper in Instructions

Pepper appearing only in cooking instructions is normally ignored.

The household is accustomed to simply skipping it.

Example:

```text
Season with pepper.
```

This does not make the meal a bad candidate.

---

## Compound Butter

Compound butter is generally adaptable.

Examples:

```text
Herb Butter
Compound Butter
Beurre Blanc Butter
```

Plain butter may be substituted when practical.

Do not automatically reject these meals.

---

## Cream Sauce Base

An integral prepared Home Chef Cream Sauce Base is a hard practical block.

The issue is not merely pepper.

The issue is that recreating or replacing the component can turn a normal meal into a substantial cooking/research project.

```text
Integral Cream Sauce Base
    ↓
DON'T WASTE THE CLICK
```

---

## Prepared Pepper-Containing Sauces

A major prepared sauce containing problematic seasoning is generally not worth investigating when replacing it would require substantial research or recreation.

This is especially important for weeknight meals.

A theoretical substitution is not enough.

If replacing the sauce turns:

```text
30-minute meal
```

into:

```text
research + shopping + recipe recreation + extended cooking
```

the meal should generally be removed from the candidate pool.

---

## Pre-Seasoned Components

Avoid pre-seasoned/prepared seasoned components when the seasoning cannot be controlled.

Examples:

```text
Pre-seasoned potatoes
Seasoned potatoes
Pre-seasoned protein
Prepared seasoned components
```

The concern is both seasoning control **and** preserving the time-saving purpose of the meal.

Do not recommend replacing a Home Chef pre-cooked component with cooking the equivalent ingredient from scratch as though that were a trivial substitution.

Also:

> Do not suggest microwaving potatoes as a workaround.

That has already proven to be an undesirable solution.

---

# Seasoning Blends

Seasoning blends are **not automatic exclusions**.

This is an important correction to the older rules.

### Known problematic blend

If the actual ingredients clearly contain a prohibited ingredient:

```text
EXCLUDE / DON'T WASTE THE CLICK
```

### Unknown blend

If Home Chef gives only something like:

```text
Southwest Seasoning
Steak Seasoning
House Seasoning
```

without enough information:

```text
🟡 REVIEW
```

Do not automatically reject it.

### Potentially replaceable blend

The household already makes and uses its own seasoning blends.

Examples of available household-style substitutions include:

* homemade chili-style blend without chilis, paprika, or pepper
* herbs de Provence
* za'atar
* garlic-based seasonings

Therefore the tool should **flag the blend and let the user decide whether an existing substitute works**.

Do not assume that an unknown blend is safe.

Do not assume that an unknown blend is automatically unusable.

---

# Spicy-Sounding Meal Titles

A spicy-sounding title is **not a first-pass rejection**.

Examples:

```text
Spicy Chicken
Chipotle Beef
Cajun Chicken
Black Pepper Steak
```

Title language is evidence, but actual ingredient/component data is more useful.

The practical workflow is:

1. First find at least three meals that actually sound appealing.
2. If there are enough good choices, spicy-sounding meals can remain lower priority.
3. If fewer than three appealing candidates survive, reconsider these meals during the second pass.

The goal is **choice**, not maximum conservatism.

---

# Minimum Candidate Rule

The practical target is:

```text
AT LEAST 3 meals the user would actually consider eating
```

The first pass should therefore be intentionally generous enough to preserve choice.

Conceptually:

```text
FULL MENU
    ↓
FIRST PASS
    ↓
obvious time-wasters removed
    ↓
Do we have ≥ 3 appealing candidates?
       │
       ├── YES → continue
       │
       └── NO → reconsider adaptable/review candidates
```

A result of zero or one technically "safe" meals is not useful if several meals could have been practically adapted.

---

# Candidate Categories

The rule engine should move toward these practical categories:

### 🟢 PROMISING

Straightforward meal with little/no adaptation required.

### 🟢 ADAPTABLE

A known, practical substitution/removal works.

Examples:

```text
Bell Pepper → remove
Garlic Pepper → garlic powder/salt
Instruction pepper → omit
Compound butter → plain butter
```

### 🟡 REVIEW

Something needs a human judgment or additional recipe inspection.

Examples:

```text
Unknown seasoning blend
Ambiguous seasoning system
Unclear prepared component
```

### 🔴 DON'T WASTE THE CLICK

The available information already indicates that investigation is unlikely to be worth the user's time.

Examples:

```text
Integral Cream Sauce Base
Major prepared pepper-containing sauce
Pre-seasoned component
Prepared component that cannot practically be adapted
```

---

# Website Workflow Discovery

The Home Chef website does not always use the exact meal title we see in other data.

A recipe URL may not take directly to the exact cart-selection page.

Example behavior observed:

A meal described as:

```text
Low-Carb Lemony Chicken Piccata
```

was actually presented in the user's available menu as:

```text
Quick Chicken Piccata
```

The user found it by visually searching the Express menu.

Therefore:

> Do not depend on exact title matching for ordering/navigation.

Preserve:

* meal ID
* recipe URL
* calendar URL when available
* meal title

The human-facing output must include a clickable Home Chef link whenever one is available.

The link is needed so the user can:

1. inspect the recipe
2. resolve ambiguous ingredients
3. locate the meal
4. add it to the cart

---

# Recent Real-World Validation

The practical rules were tested against an actual Home Chef selection.

Final selected meals for the September 2 delivery were:

```text
Tzatziki Trout
Rotisserie-Style Chicken with Herb Butter
Pork Chop with Pear-Fig Chutney
Quick Chicken Piccata
```

The order also included:

```text
Cheddar & Monterey Grilled Cheese
Caramel Apple Blossoms
```

The four entrée choices demonstrate useful variety:

```text
Fish
Chicken
Pork
Chicken
```

and included both standard meal kits and an Express meal.

The Rotisserie-Style Chicken meal also demonstrated that a broth concentrate can be practically substituted when the household has an appropriate Better Than Bouillon-style replacement, while the seasoning can be recreated from known ingredients.

This is a useful example of why **practical adaptability** matters more than simplistic keyword rejection.

---

# Tier / Cost Priority

Meal tier is separate from pepper/safety/practical classification.

Preferred ordering priority:

```text
Standard
    ↓
Culinary Collection
    ↓
Premium
```

A more expensive Culinary Collection meal should not automatically displace a practical Standard meal merely because it looks appealing.

A Culinary Collection meal can still be useful when the Standard pool is insufficient.

Premium should generally be fallback rather than automatically promoted.

Important:

```text
Premium ≠ difficult
Culinary Collection ≠ difficult
```

Tier describes purchasing/pricing priority, not cooking effort.

---

# Current Technical Milestone

The project is currently at:

```text
structured Home Chef JSON
        ↓
existing parser
        ↓
normalized meal objects
        ↓
PRACTICAL RULE ENGINE  ← next major work
        ↓
candidate classification
        ↓
shortlist
        ↓
human selection
```

Do **not** restart the project.

Do **not** rebuild the HTML scraper.

Do **not** solve Cloudflare.

Do **not** build a dashboard.

Do **not** add unrelated integrations.

---

# Next Development Session

Start with:

```powershell
cd C:\Users\jschw\GitHub\home-chef-safe-menu\repo
.\.venv\Scripts\Activate.ps1
git status
python -m pytest
```

Then inspect:

```text
src/parser.py
src/rules.py
src/output.py
tests/test_parser.py
```

Specifically determine:

1. What normalized fields the parser currently produces.
2. What the current rule engine expects.
3. What tests already exist.
4. What the smallest missing connection is.

Then add **one behavior test** for the practical screening model.

Good first real cases:

```text
Bell Pepper → adaptable
Garlic Pepper → adaptable
Instruction-only pepper → adaptable
Compound Butter → adaptable
Cream Sauce Base → don't waste the click
Pre-seasoned component → don't waste the click
Unknown seasoning blend → review
```

Implement only the smallest behavior required by the test.

Run:

```powershell
python -m pytest
```

Inspect the actual output before making the next change.

---

# Git / Documentation State

The previous README merge conflict has been resolved.

Do not reopen or recreate that conflict.

`README.md` and the Master Project Notes should not become competing sources of truth.

Use:

```text
README.md
    ↓
project-facing documentation

Master Project Notes
    ↓
authoritative project behavior/architecture/rules

Session Handoff
    ↓
where development resumes next time
```

Do not turn the Session Handoff into a daily journal.

Only add information that will materially help resume work.

---

# Important Stopping Rule

Work in small milestones.

For each meaningful change:

```text
inspect
→ change one thing
→ test
→ inspect output
→ fix specific problem
→ test again
→ commit
→ stop
```

When the current milestone works:

> **STOP.**

Do not invent additional work just because it could eventually be useful.

---

# Immediate Resume Point

The next useful technical question is:

> **Can the existing normalized Home Chef meal objects be passed cleanly into a practical rule engine that distinguishes PROMISING, ADAPTABLE, REVIEW, and DON'T WASTE THE CLICK?**

That is where development should resume.

The parser discovery is done.

The practical household rules are now much clearer.

The next step is to encode those rules **carefully and test-first**, using the real captured menu data rather than inventing a giant speculative keyword list.
