"""Property-based fuzzing tests, with a small offline fallback corpus."""

import pytest

try:
    from hypothesis import given, strategies as st
except ModuleNotFoundError:  # Hypothesis is listed in requirements.txt.
    HYPOTHESIS_AVAILABLE = False
else:
    HYPOTHESIS_AVAILABLE = True

from processor import parse_vitals_summary, compute_patient_bmi, assign_ward_bed


def _no_crash(function, value):
    try:
        result = function(value)
    except Exception as exc:
        pytest.fail(f"{function.__name__} crashed for {value!r}: {exc}")
    assert result is None or isinstance(result, (str, float))


@pytest.mark.parametrize("value, expected", [
    ("80,98,37", "Vitals: HR=80.0, SpO2=98.0% - STABLE"),
    ("130,85,40", "Vitals: HR=130.0, SpO2=85.0% - CRITICAL"),
])
def test_valid_vitals_summary(value, expected):
    assert parse_vitals_summary(value) == expected


def test_valid_bmi():
    assert compute_patient_bmi("70/1.75") == 22.86


def test_bmi_extreme_height_is_safe():
    assert compute_patient_bmi("1/1e-300") is None


def test_valid_ward_bed():
    assert assign_ward_bed("icu-05") == "Intensive Care Unit Bed #5"


if HYPOTHESIS_AVAILABLE:
    @given(st.text() | st.none())
    def test_parse_vitals_summary_no_crash(s):
        _no_crash(parse_vitals_summary, s)

    @given(st.text() | st.none())
    def test_compute_patient_bmi_safe(s):
        _no_crash(compute_patient_bmi, s)

    @given(st.text() | st.none())
    def test_assign_ward_bed_safe(s):
        _no_crash(assign_ward_bed, s)
else:
    # Deterministic malformed examples keep local verification possible offline.
    @pytest.mark.parametrize("s", [None, "", "1,2", "x,2,3", "1,2,3,4"])
    def test_parse_vitals_summary_no_crash(s):
        _no_crash(parse_vitals_summary, s)

    @pytest.mark.parametrize("s", [None, "", "70", "70/0", "x/1.75"])
    def test_compute_patient_bmi_safe(s):
        _no_crash(compute_patient_bmi, s)

    @pytest.mark.parametrize("s", [None, "", "ICU", "BAD-5", "ICU-0"])
    def test_assign_ward_bed_safe(s):
        _no_crash(assign_ward_bed, s)
