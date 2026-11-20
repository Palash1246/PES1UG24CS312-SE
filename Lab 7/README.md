# Lab 7 - Fuzz Testing with Hypothesis

Install `python -m pip install -r requirements.txt`, then run `python -m pytest -q test_processor.py`.

The three Hypothesis properties fuzz arbitrary strings and `None`. Invalid inputs return `None`; valid inputs keep the original formatted result.

Run the interactive demo with `python processor.py`.
