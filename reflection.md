# Lab 5: Reflection

## 1. Which issues were the easiest and which were the hardest to fix?

The easiest were the mechanical ones: Flake8's blank-line and line-length errors, the f-string, the snake_case rename, and the docstrings. The tools say exactly what to change, and nothing about program behavior shifts. The hardest was the bare `except: pass`. Deleting it would not have been enough, because it was hiding real problems. The string `"full"` raised a `TypeError` and an empty route would have raised `ZeroDivisionError`, and both were silently ignored. To fix it properly I had to decide what the program should do with bad data, so I added validation in `add_trip_log` and made `average_load` return `None` for a route with no trips. The mutable default `logs=[]` was also easy to fix but needed thought, because the shared list would not have shown up in a single run.

## 2. Did the tools report any false positives, and how did you decide?

Bandit's B311 (`random.choice`) is close to a false positive. Picking a shuttle driver is not a security decision, so no real vulnerability exists. I still switched to `secrets.choice` because it is a one-line change with no downside and the lab asks for all Bandit findings to be handled. I preferred that to a `# nosec` comment, which only silences the warning. Pylint's unused-argument warning on `assign_driver` was valid but pointed at a design gap rather than dead code: the function never checked that the route existed, so I made it use the argument. To judge a finding, I ask whether it could actually cause harm in this program and how costly the fix is.

## 3. How would you integrate static analysis into your regular workflow?

I would run Flake8 and Pylint in the editor while coding, so the feedback is immediate. A pre-commit hook would run all three tools before each commit, and the same checks would run in CI (for example GitHub Actions) on every pull request, failing the build on Bandit findings and on a Pylint score below a set threshold. That keeps style arguments out of code review. For issues I deliberately accept, I would add a documented suppression with a reason instead of leaving the warning in the report.

## 4. What tangible improvements in quality, security and readability did you see?

The Pylint score went from 6.25 to 10.00, and Bandit and Flake8 now report nothing. More importantly, the program behaves better: negative and non-numeric passenger counts are rejected with a clear message, R2's average is no longer -1.0, an unknown route no longer crashes the script, and the program no longer ends in a `KeyError` traceback. Files are closed properly, the module can be imported without running the demo, and every function has a docstring. The lab also showed me that the tools do not find everything. The wrong-looking output (a negative average, the final crash) only showed up when I ran the program and read its output, so static analysis complements running and testing the code and does not replace them.
