"""Input-safe patient summary and ward allocation helpers."""

import math


def parse_vitals_summary(vitals_csv):
    """Return a summary for HR, SpO2 and temperature, or None if invalid."""
    if not isinstance(vitals_csv, str):
        return None
    parts = [part.strip() for part in vitals_csv.split(",")]
    if len(parts) != 3:
        return None
    try:
        hr, spo2, temp = (float(part) for part in parts)
    except (TypeError, ValueError):
        return None
    if not all(math.isfinite(value) for value in (hr, spo2, temp)):
        return None
    critical = hr > 120 or spo2 < 90 or temp > 39.0
    return f"Vitals: HR={hr}, SpO2={spo2}% - {'CRITICAL' if critical else 'STABLE'}"


def compute_patient_bmi(bmi_string):
    """Compute BMI from 'weight/height'; return None for malformed values."""
    if not isinstance(bmi_string, str):
        return None
    parts = bmi_string.split("/")
    if len(parts) != 2:
        return None
    try:
        weight, height = (float(part.strip()) for part in parts)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(weight) or not math.isfinite(height) or weight <= 0 or height <= 0:
        return None
    try:
        bmi = weight / (height ** 2)
    except (OverflowError, ZeroDivisionError):
        return None
    if not math.isfinite(bmi):
        return None
    return round(bmi, 2)


def assign_ward_bed(allocation_code):
    """Format a known ward and positive bed number; return None if invalid."""
    if not isinstance(allocation_code, str):
        return None
    parts = allocation_code.strip().split("-")
    if len(parts) != 2:
        return None
    ward, bed_str = (part.strip() for part in parts)
    ward_names = {"ER": "Emergency Room", "ICU": "Intensive Care Unit", "GEN": "General Ward", "PED": "Pediatrics"}
    try:
        bed_num = int(bed_str)
    except (TypeError, ValueError):
        return None
    if ward.upper() not in ward_names or bed_num <= 0:
        return None
    return f"{ward_names[ward.upper()]} Bed #{bed_num}"


def main():
    print("==== Running parse_vitals_summary ====")
    v_input = input("Enter vitals (HR,SpO2,Temp): ")
    print("Summary:", parse_vitals_summary(v_input))
    print("\n==== Running compute_patient_bmi ====")
    b_input = input("Enter weight/height (e.g. 70/1.75): ")
    print("BMI:", compute_patient_bmi(b_input))
    print("\n==== Running assign_ward_bed ====")
    w_input = input("Enter allocation (e.g. ICU-05): ")
    print("Assignment:", assign_ward_bed(w_input))


if __name__ == "__main__":
    main()
