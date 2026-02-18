Limit your review to only `source/*` and `output/*`. Ignore all other changes.

Prioritize the following under `source/*`:
- Flag any unexplained, hardcoded numerical values.
- Flag saving data to file that is done not through SaveData function; Suggest changes using `SaveData()` (syntax is documented in `source/lib/SaveData.py` for Python version and https://github.com/gslab-econ/gslab_r/tree/master/SaveData for R version)
- Flag added code with variable / function / dataframe column naming conventions that deviates from the existing naming convention in the repo
  - e.g. if the original repo always names objects in snake_case + functions in PascalCase + static scalars in ALL_CAPS, while the new code introduced in this PR violates these conventions, flag it.
- Flag scripts that are not written in modular form, a `Main`/`main` function
- Flag any script (excluding those in `source/lib`) that routinely uses trivial / obvious code documention such as inline comments or function docstrings. Non-library scripts should be self-documenting with minimal documentation.
  - Never suggest any changes that adds any inline comments or docstrings

If you can't complete all of the above, flag in the review comment that you didn't flag everything and that the user should request another review from you. Once the above is reviewed, move on to `output/*` if and only if you have extra bandwidth. In `output/` prioritize reviewing log files over other files.

Ignore the following issues, for we consider them trivial:
- Trailing/leading spaces
