# Lab 6 - Hospital Triage Priority

The starter application is tested independently for statement coverage and branch coverage.

- `CodeCoverageTest_hospital_triage_priority.py`: line coverage run.
- `BranchCoverageTest_hospital_triage_priority.py`: branch coverage run.
- `evidence/`: terminal output captures for both measured runs.

From this directory, use `python -m coverage run --source=hospital_triage_priority -m pytest -q CodeCoverageTest_hospital_triage_priority.py` and `python -m coverage report -m`. For branch coverage, add `--branch` and use the branch test filename.
