import pytest
from hospital_triage_priority import process_triage_wards, monitor_oxygen_manifolds


def test_invalid_wards_type():
    with pytest.raises(ValueError):
        process_triage_wards({}, 10)


def test_negative_default_score():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_non_accepting_ward_is_skipped():
    assert process_triage_wards([{"is_accepting": False, "patients": [{"spo2": 1}]}], 10) == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_accepted_empty_ward_default_tier_and_defaults():
    assert process_triage_wards([{"is_accepting": True, "patients": [{}]}], 10) == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


def test_invalid_vitals_count_as_flagged_and_skip_acuity():
    patients = [{"spo2": 0}, {"hr": 0}]
    assert process_triage_wards([{"is_accepting": True, "patients": patients}], 10)["acuity_score"] == 0


def test_unconscious_in_general_ward_adds_critical_acuity():
    result = process_triage_wards([{"is_accepting": True, "patients": [{"unconscious": True}]}], 10)
    assert result == {"acuity_score": 100, "status": "TRIAGE_STABLE"}


def test_unconscious_outpatient_resets_total_and_breaks_patient_loop():
    wards = [{"is_accepting": True, "tier": "outpatient", "patients": [{"spo2": 80}, {"unconscious": True}, {"spo2": 80}]}]
    assert process_triage_wards(wards, 10)["acuity_score"] == 0


def test_low_oxygen_or_high_heart_rate_adds_60():
    wards = [{"is_accepting": True, "patients": [{"spo2": 89}, {"hr": 121}]}]
    assert process_triage_wards(wards, 10)["acuity_score"] == 120


def test_icu_standby_adds_25():
    result = process_triage_wards([{"is_accepting": True, "icu_standby": True}], 10)
    assert result == {"acuity_score": 25, "status": "TRIAGE_STABLE"}


def test_more_than_four_invalid_entries_triggers_alert():
    patients = [{"spo2": 0} for _ in range(5)]
    result = process_triage_wards([{"is_accepting": True, "patients": patients}], 10)
    assert result["status"] == "WARD_ALERT"


def test_exactly_four_invalid_entries_does_not_trigger_alert():
    patients = [{"hr": 0} for _ in range(4)]
    assert process_triage_wards([{"is_accepting": True, "patients": patients}], 10)["status"] == "NO_URGENT_CASES"


def test_no_oxygen_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_single_low_pressure_is_recovered():
    assert monitor_oxygen_manifolds([[3.9, 4.0]]) == "PRESSURE_NORMAL"


def test_two_consecutive_low_readings_fail():
    assert monitor_oxygen_manifolds([[4.0, 3.9, 3.8, 5.0]]) == "PRESSURE_FAILURE"


def test_pressure_streak_resets_at_normal_value():
    assert monitor_oxygen_manifolds([[3.0, 4.1, 3.0], [4.0]]) == "PRESSURE_NORMAL"
