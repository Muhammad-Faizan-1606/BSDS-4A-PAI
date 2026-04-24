"""
tests/test_prolog_engine.py
Unit tests for the Prolog engine and OCR parsing utilities.
Run: python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))

import pytest
from ocr import parse_dose_mg, parse_frequency_per_day, normalize_medicine_name
from drug_fallback import DRUG_INTERACTIONS_JSON, MAX_DOSES_JSON, SIDE_EFFECTS_JSON


# ============================================================
# Tests for OCR utility functions
# ============================================================

class TestParseDoseMg:
    def test_milligrams(self):
        assert parse_dose_mg("500mg") == 500.0

    def test_milligrams_with_space(self):
        assert parse_dose_mg("250 mg") == 250.0

    def test_grams_conversion(self):
        assert parse_dose_mg("1g") == 1000.0

    def test_micrograms_conversion(self):
        assert parse_dose_mg("100mcg") == 0.1

    def test_empty_string(self):
        assert parse_dose_mg("") == 0.0

    def test_no_unit(self):
        assert parse_dose_mg("500") == 0.0

    def test_decimal_dose(self):
        assert parse_dose_mg("2.5mg") == 2.5


class TestParseFrequencyPerDay:
    def test_once_daily(self):
        assert parse_frequency_per_day("once daily") == 1

    def test_twice_daily(self):
        assert parse_frequency_per_day("twice daily") == 2

    def test_bd(self):
        assert parse_frequency_per_day("BD") == 2

    def test_tds(self):
        assert parse_frequency_per_day("TDS") == 3

    def test_three_times(self):
        assert parse_frequency_per_day("three times a day") == 3

    def test_qds(self):
        assert parse_frequency_per_day("QDS") == 4

    def test_unknown_defaults_to_one(self):
        assert parse_frequency_per_day("unclear") == 1


class TestNormalizeMedicineName:
    def test_tab_prefix(self):
        result = normalize_medicine_name("Tab. Paracetamol")
        assert "paracetamol" in result.lower()

    def test_cap_prefix(self):
        result = normalize_medicine_name("Cap. Amoxicillin")
        assert "amoxicillin" in result.lower()

    def test_no_prefix(self):
        result = normalize_medicine_name("Warfarin")
        assert result == "Warfarin"


# ============================================================
# Tests for drug fallback database
# ============================================================

class TestDrugInteractionsDatabase:
    def test_warfarin_aspirin_is_danger(self):
        key = tuple(sorted(["warfarin", "aspirin"]))
        assert key in DRUG_INTERACTIONS_JSON
        assert DRUG_INTERACTIONS_JSON[key]["severity"] == "danger"

    def test_all_entries_have_severity(self):
        for key, val in DRUG_INTERACTIONS_JSON.items():
            assert "severity" in val, f"Missing severity for {key}"
            assert val["severity"] in ["danger", "warning", "ok"]

    def test_all_entries_have_description(self):
        for key, val in DRUG_INTERACTIONS_JSON.items():
            assert "description" in val
            assert len(val["description"]) > 10


class TestMaxDosesDatabase:
    def test_paracetamol_max(self):
        assert MAX_DOSES_JSON["paracetamol"] == 4000

    def test_ibuprofen_max(self):
        assert MAX_DOSES_JSON["ibuprofen"] == 2400

    def test_warfarin_max(self):
        assert MAX_DOSES_JSON["warfarin"] == 15

    def test_all_doses_positive(self):
        for drug, dose in MAX_DOSES_JSON.items():
            assert dose > 0, f"Invalid dose for {drug}"


class TestSideEffectsDatabase:
    def test_warfarin_has_bleeding_risk(self):
        assert "bleeding_risk" in SIDE_EFFECTS_JSON.get("warfarin", [])

    def test_metformin_has_nausea(self):
        assert "nausea" in SIDE_EFFECTS_JSON.get("metformin", [])

    def test_all_effects_are_lists(self):
        for drug, effects in SIDE_EFFECTS_JSON.items():
            assert isinstance(effects, list), f"Effects for {drug} must be a list"
            assert len(effects) > 0, f"Empty effects list for {drug}"


# ============================================================
# Tests for risk calculation
# ============================================================

class TestRiskCalculation:
    def setup_method(self):
        """Import the calculate_risk function from app"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))

    def test_no_interactions_gives_high_score(self):
        from app import calculate_risk
        score, risk = calculate_risk([], [])
        assert score == 100
        assert risk == "Low"

    def test_one_danger_lowers_score(self):
        from app import calculate_risk
        interactions = [{"severity": "danger"}]
        score, risk = calculate_risk(interactions, [])
        assert score == 70
        assert risk == "Low"

    def test_multiple_dangers_give_high_risk(self):
        from app import calculate_risk
        interactions = [{"severity": "danger"}, {"severity": "danger"}, {"severity": "danger"}]
        score, risk = calculate_risk(interactions, [])
        assert score == 10
        assert risk == "High"

    def test_warnings_give_moderate_risk(self):
        from app import calculate_risk
        interactions = [{"severity": "warning"}, {"severity": "warning"}, {"severity": "warning"}]
        score, risk = calculate_risk(interactions, [])
        assert score == 70
        assert risk == "Low"

    def test_score_never_goes_below_zero(self):
        from app import calculate_risk
        interactions = [{"severity": "danger"}] * 10
        score, _ = calculate_risk(interactions, [])
        assert score >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
