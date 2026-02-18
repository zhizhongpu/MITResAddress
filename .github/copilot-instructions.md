Prioritize the following:
- Flag any unexplained, hardcoded numerical values.
- Flag saving data to file that is done not through SaveData function; Suggest changes using `SaveData()` (syntax is documented in `source/lib/SaveData.py` for Python version and https://github.com/gslab-econ/gslab_r/tree/master/SaveData for R version)
- Flag added code with variable / function / dataframe column naming convention that deviates from the existing naming convention in the repo
- Flag scripts that are not written in modular form, a `Main`/`main` function
- Flag any script (excluding those in `source/lib`) that routinely uses trivial / obvious code documention such as inline comments or function docstrings. Non-library scripts should be self-documenting with minimal documentation.

If you can't complete all of the above, flag in the review comment that you didn't flag everything and that the user should request another review from you.

Deprioritize any changes in the output/ directory, unless you have extra bandwidth. In that case, prioritize reviewing log files.
