Prioritize the following:
- Flag any hardcoded values except for file paths and names.
- Flag any exporting to csv using non-SaveData functions.
- Flag violations of the following variable naming conventions:
  - All variables should be lowercase except for static variables which should be ALL CAPS.
  - All functions should be PascalCase.
  - All other objects should be snake_case.
- Flag scripts that are not written in the [modular form, with the first function being the `Main` function]
- Flag changes in scripts and outputs that are not reflected in changes in SConscript files.

If you can't complete all of the above, flag in the review comment that you didn't flag everything and that the user should request another review from you.

Deprioritize any changes in the output/ directory, unless you have extra bandwidth. In that case, prioritize log files.
