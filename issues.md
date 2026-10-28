# Lab 5: Issues Found in `shuttle_system.py`

Line numbers refer to the **original** file. Rows are ordered by severity (high/medium first). Tool severity is Bandit's own rating; for the rest, severity is my judgment of the impact on the program.

Scores: Pylint **6.25 → 10.00**, Bandit **2 → 0** issues, Flake8 **10 → 0** issues.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Bare `except: pass` hides errors (Bandit B110, Pylint W0702, Flake8 E722) | Bug / Quality (High) | 26-30 | Swallows every exception, including the `TypeError` from the string `"full"` and the `ZeroDivisionError` from a route with no trips. Bad data was silently ignored and R3 was never reported. | Removed the `try/except`. `average_load` now returns `None` when there are no trips and `underused_routes` checks for that explicitly. Bad data is rejected at input instead (next row). |
| Invalid passenger counts accepted (not flagged by any tool) | Bug (High) | 11-14, 49-50 | `-6` and `"full"` were stored. R2's average became `-1.0` and R3's trip list became `["full"]`, which would crash `sum()`. | `add_trip_log` validates that the count is a non-negative whole number and raises `ValueError`; `main` catches it and prints "Skipped trip". |
| Crash with `KeyError` on removed or unknown route (not flagged by any tool) | Bug (High) | 55-58 | `average_load("R3")` runs after `remove_route("R3")`, so the program always ended in a traceback. Typing an unknown route (e.g. `R9`) at the prompt also crashed. | `main` checks `choice in routes` and `"R3" in routes` before looking up, and prints a clear message instead. |
| Mutable default argument `logs=[]` (Pylint W0102) | Bug (Medium) | 11 | The same list is shared across every call, so log lines from unrelated calls pile up in one list. | Default changed to `None`; a new list is created inside the function when needed. `main` passes its own list. |
| Weak random generator `random.choice` (Bandit B311, Low severity) | Security (Medium/Low) | 2, 35 | `random` is not cryptographically secure. In this program, picking a driver is not security-sensitive, so this is close to a false positive, but the tool flags it. | Replaced with `secrets.choice` and moved the driver names to a `DRIVERS` constant. Chose this over `# nosec` so the warning is fixed rather than hidden. |
| Files opened without `with` and without encoding (Pylint R1732, W1514) | Resource leak (Medium) | 39-43 | The second `open()` is never closed, and a failed write would leave the first one open. No encoding means behavior depends on the OS. | Used `with open(..., encoding="utf-8")` and `json.dump` / `json.load`. |
| `global routes` statement (Pylint W0603) | Design (Medium) | 38 | Rebinding a module global inside a function makes the data flow hard to follow and test. | Reload into the existing dict with `routes.clear()` and `routes.update(saved)`, so no `global` is needed. |
| Unused argument `route_id` (Pylint W0613) | Maintainability (Low) | 33 | `assignDriver` ignores its parameter, so it would happily "assign" a driver to a route that does not exist. | The argument is now used: raises `KeyError` for an unknown route before choosing a driver. |
| Function name `assignDriver` (Pylint C0103) | Style (Low) | 33 | camelCase breaks Python's snake_case naming convention. | Renamed to `assign_driver` and updated the call in `main`. |
| Missing module and function docstrings (Pylint C0114, C0116 ×8) | Documentation (Low) | 1, 11, 16, 19, 23, 33, 37, 45 | No description of what the module or any function does. | Added a module docstring and one for every function. |
| `%` string formatting (Pylint C0209) | Style (Low) | 13 | Old-style formatting is harder to read than an f-string. | Converted to an f-string. |
| Missing blank lines (Flake8 E302 ×7, E305) | Style (Low) | 11, 16, 19, 23, 33, 37, 45, 60 | PEP 8 needs two blank lines around top-level definitions. | Added the blank lines. |
| Line too long, 82 > 79 (Flake8 E501) | Style (Low) | 13 | Line exceeds PEP 8 length. | Wrapped across lines (also wrapped the new validation lines I added). |
| `main()` runs on import (not flagged by any tool) | Design (Low) | 60 | Importing the module would immediately run the demo and prompt for input. | Wrapped in `if __name__ == "__main__":`. |
