Prioritize the following:
- Flag any hardcoded values.
- Flag any exporting to csv using non-SaveData functions.
- Flag violoations of the following variable naming conventions:
  - All variables should be lowercase except for static variables which should be ALL CAPS.
  - All functions should be PascalCase.
  - All other objects should be snake_case.
- Flag scripts that are not written in the [modular form, with the first function being the `Main` function]
- Flag scripts not part of the SCons build, as specified in the SConscript files.

Deprioritize any changes in the output/ directory, unless you have extra bandwidth. In that case, prioritize log files.
