# RecipeTestKitchen

A recipe workspace for meals you want to try, test, rate, and promote into keepers.

## Structure
- `recipes/to-try/` - recipes you want to make soon
- `recipes/tested/` - recipes you have made and reviewed
- `recipes/keepers/` - recipes worth keeping and repeating
- `RECIPE_INDEX.md` - master list of recipes by section
- `RECIPE_BOOK.md` - generated all-in-one recipe book
- `MISSING_PIECES.md` - reminder list for recipes with missing source pages
- `templates/recipe-template.md` - template for new recipe files
- `scripts/generate_recipe_book.py` - rebuilds `RECIPE_BOOK.md`

## Quick Start
1. Copy `templates/recipe-template.md` to the right folder under `recipes/`.
2. Fill in the recipe details, estimated calories/macros, and notes after you make it.
3. Add a link to the recipe in the matching section of `RECIPE_INDEX.md`.
4. Run `python3 scripts/generate_recipe_book.py` to rebuild `RECIPE_BOOK.md`.

## Suggested Workflow
- Start new ideas in `recipes/to-try/`.
- Move them to `recipes/tested/` after you make them and add your rating.
- Move your winners to `recipes/keepers/` when they earn a permanent spot.

## Current Follow-Up
- Check [MISSING_PIECES.md](/Users/kristine.kartchner/Documents/RecipeTestKitchen/MISSING_PIECES.md) for recipes that still need missing cookbook pages.
