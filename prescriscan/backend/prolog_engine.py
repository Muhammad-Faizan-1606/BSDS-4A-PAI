"""
prolog_engine.py - Python bridge to SWI-Prolog knowledge base
Uses pyswip library to query drug interaction rules in real-time.

Install: pip install pyswip
Requires: SWI-Prolog installed on system (https://www.swi-prolog.org/Download.html)
"""

import os
from itertools import combinations

# Try to import pyswip; fall back to JSON-based lookup if not installed
try:
    from pyswip import Prolog
    PROLOG_AVAILABLE = True
except ImportError:
    PROLOG_AVAILABLE = False
    print("WARNING: pyswip not installed. Using JSON fallback mode.")
    print("Run: pip install pyswip")

from drug_fallback import DRUG_INTERACTIONS_JSON, MAX_DOSES_JSON, SIDE_EFFECTS_JSON


class PrologEngine:
    """
    Wraps SWI-Prolog for drug interaction queries.
    Falls back to JSON lookup if Prolog is not installed.
    """

    def __init__(self, kb_path: str = "../knowledge_base/drug_interactions.pl"):
        self.kb_path = os.path.abspath(kb_path)
        self.prolog = None
        self._ready = False

        if PROLOG_AVAILABLE and os.path.exists(self.kb_path):
            try:
                self.prolog = Prolog()
                self.prolog.consult(self.kb_path)
                self._ready = True
                print(f"Prolog engine loaded: {self.kb_path}")
            except Exception as e:
                print(f"Prolog load error: {e}. Using JSON fallback.")
        else:
            print("Prolog engine in JSON fallback mode.")

    def is_ready(self) -> bool:
        return self._ready

    def check_interactions(self, medicine_names: list) -> list:
        """
        Check all pairwise drug interactions for a list of medicines.

        Args:
            medicine_names: list of lowercase medicine name strings

        Returns:
            list of interaction dicts with keys: drugs, severity, description
        """
        results = []
        pairs = list(combinations(medicine_names, 2))

        for drug_a, drug_b in pairs:
            interaction = self._query_interaction(drug_a, drug_b)
            if interaction:
                results.append(interaction)

        if not results:
            results.append({
                "drugs": medicine_names,
                "severity": "ok",
                "description": "No significant interactions detected between the prescribed medicines."
            })

        return results

    def _query_interaction(self, drug_a: str, drug_b: str) -> dict | None:
        """Query Prolog for interaction between two drugs."""

        if self._ready and self.prolog:
            # Real Prolog query: interacts(Drug1, Drug2, Severity, Description)
            query = f"interacts({drug_a}, {drug_b}, Severity, Description)"
            try:
                solutions = list(self.prolog.query(query))
                if not solutions:
                    # Try reverse order
                    query = f"interacts({drug_b}, {drug_a}, Severity, Description)"
                    solutions = list(self.prolog.query(query))

                if solutions:
                    sol = solutions[0]
                    return {
                        "drugs": [drug_a.title(), drug_b.title()],
                        "severity": str(sol["Severity"]),
                        "description": str(sol["Description"])
                    }
            except Exception as e:
                print(f"Prolog query error: {e}")

        # JSON fallback
        key = tuple(sorted([drug_a, drug_b]))
        fallback = DRUG_INTERACTIONS_JSON.get(key)
        if fallback:
            return {
                "drugs": [drug_a.title(), drug_b.title()],
                "severity": fallback["severity"],
                "description": fallback["description"]
            }

        return None

    def check_dosages(self, medicines: list) -> list:
        """
        Validate dosages for each medicine against Prolog max_dose facts.

        Args:
            medicines: list of dicts with keys: name, dose, frequency

        Returns:
            list of dosage check results
        """
        from ocr import parse_dose_mg, parse_frequency_per_day

        results = []

        for med in medicines:
            name = med.get("name", "").lower()
            dose_str = med.get("dose", "0mg")
            freq_str = med.get("frequency", "once daily")

            dose_mg = parse_dose_mg(dose_str)
            times_per_day = parse_frequency_per_day(freq_str)
            daily_dose = dose_mg * times_per_day

            max_dose = self._get_max_dose(name)

            if max_dose is None:
                status = "ok"
                note = "No maximum dose data available in knowledge base."
                max_display = "Unknown"
            elif daily_dose > max_dose:
                status = "danger"
                note = f"EXCEEDS maximum safe daily dose! Prescribed {daily_dose}mg/day, max is {max_dose}mg/day."
                max_display = f"{max_dose}mg/day"
            elif daily_dose > max_dose * 0.8:
                status = "warning"
                note = f"Close to maximum safe dose. Monitor carefully."
                max_display = f"{max_dose}mg/day"
            else:
                status = "ok"
                note = "Within safe dosage range."
                max_display = f"{max_dose}mg/day"

            results.append({
                "medicine": med.get("name", name.title()),
                "prescribed_dose": f"{daily_dose}mg/day" if daily_dose > 0 else dose_str,
                "max_safe_dose": max_display,
                "status": status,
                "note": note
            })

        return results

    def _get_max_dose(self, drug_name: str) -> float | None:
        """Query Prolog for max safe daily dose of a drug."""

        if self._ready and self.prolog:
            try:
                solutions = list(self.prolog.query(f"max_dose({drug_name}, MaxDose)"))
                if solutions:
                    return float(solutions[0]["MaxDose"])
            except Exception:
                pass

        # JSON fallback
        return MAX_DOSES_JSON.get(drug_name)

    def get_side_effects(self, medicine_names: list) -> list:
        """
        Get known side effects for each medicine from Prolog.

        Returns:
            list of dicts with keys: medicine, effects
        """
        results = []

        for name in medicine_names:
            effects = self._query_side_effects(name)
            if effects:
                results.append({
                    "medicine": name.title(),
                    "effects": effects
                })

        return results

    def _query_side_effects(self, drug_name: str) -> list:
        """Query Prolog for all side effects of a drug."""

        if self._ready and self.prolog:
            try:
                solutions = list(self.prolog.query(f"side_effect({drug_name}, Effect)"))
                if solutions:
                    return [str(s["Effect"]) for s in solutions]
            except Exception:
                pass

        # JSON fallback
        return SIDE_EFFECTS_JSON.get(drug_name, [])
