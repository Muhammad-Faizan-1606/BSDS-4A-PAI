"""
drug_fallback.py - JSON fallback database for when SWI-Prolog is not installed.
This mirrors the Prolog knowledge base facts in Python dictionaries.
In production, all queries go through the Prolog engine instead.
"""

# Drug-drug interactions: key = sorted tuple of two drug names
# Format: {("drug_a", "drug_b"): {"severity": "danger|warning|ok", "description": "..."}}
DRUG_INTERACTIONS_JSON = {
    ("aspirin", "warfarin"): {
        "severity": "danger",
        "description": "Serious bleeding risk. Both drugs impair clotting — concurrent use greatly increases hemorrhage risk. Requires immediate physician review."
    },
    ("ibuprofen", "warfarin"): {
        "severity": "danger",
        "description": "NSAIDs like ibuprofen significantly potentiate warfarin's anticoagulant effect, raising risk of serious bleeding episodes."
    },
    ("maoi", "ssri"): {
        "severity": "danger",
        "description": "Potentially fatal serotonin syndrome. These drug classes must NEVER be combined. Washout period of at least 14 days required."
    },
    ("maoi", "tramadol"): {
        "severity": "danger",
        "description": "Risk of serotonin syndrome and seizures. Contraindicated combination."
    },
    ("clopidogrel", "omeprazole"): {
        "severity": "warning",
        "description": "Omeprazole reduces activation of clopidogrel via CYP2C19 inhibition, potentially reducing its antiplatelet effect."
    },
    ("metformin", "contrast_dye"): {
        "severity": "warning",
        "description": "Metformin should be withheld before contrast procedures due to risk of lactic acidosis."
    },
    ("digoxin", "amiodarone"): {
        "severity": "warning",
        "description": "Amiodarone raises digoxin plasma levels significantly. Digoxin dose reduction of 50% may be required."
    },
    ("amlodipine", "simvastatin"): {
        "severity": "warning",
        "description": "Amlodipine inhibits simvastatin metabolism, increasing risk of muscle toxicity (myopathy). Consider dose adjustment."
    },
    ("ciprofloxacin", "theophylline"): {
        "severity": "warning",
        "description": "Ciprofloxacin inhibits theophylline metabolism, raising its plasma level and risk of toxicity."
    },
    ("ace_inhibitor", "potassium"): {
        "severity": "warning",
        "description": "ACE inhibitors reduce potassium excretion. Combined with potassium supplements, risk of dangerous hyperkalemia."
    },
    ("methotrexate", "nsaid"): {
        "severity": "danger",
        "description": "NSAIDs reduce methotrexate clearance, causing toxic accumulation. Severe bone marrow suppression possible."
    },
    ("lithium", "nsaid"): {
        "severity": "danger",
        "description": "NSAIDs reduce lithium renal clearance, causing lithium toxicity. Monitor lithium levels closely."
    }
}

# Maximum safe daily doses in mg
MAX_DOSES_JSON = {
    "paracetamol": 4000,
    "acetaminophen": 4000,
    "ibuprofen": 2400,
    "aspirin": 4000,
    "warfarin": 15,
    "metformin": 3000,
    "amoxicillin": 3000,
    "amoxicillin_clavulanate": 3000,
    "ciprofloxacin": 1500,
    "azithromycin": 500,
    "omeprazole": 80,
    "pantoprazole": 80,
    "atorvastatin": 80,
    "simvastatin": 80,
    "amlodipine": 10,
    "lisinopril": 80,
    "metoprolol": 400,
    "losartan": 100,
    "levothyroxine": 0.3,  # 300mcg = 0.3mg
    "digoxin": 0.375,
    "diazepam": 40,
    "tramadol": 400,
    "codeine": 240,
    "morphine": 200,
    "prednisone": 80,
    "prednisolone": 80,
    "dexamethasone": 40,
    "salbutamol": 32,  # inhaled puffs converted
    "cetirizine": 10,
    "loratadine": 10,
    "chlorphenamine": 24,
    "metronidazole": 2000,
    "fluconazole": 400,
    "acyclovir": 4000,
    "sertraline": 200,
    "fluoxetine": 80,
    "escitalopram": 20,
    "clonazepam": 20,
    "alprazolam": 4,
}

# Known side effects per drug
SIDE_EFFECTS_JSON = {
    "warfarin": ["bleeding_risk", "bruising", "nosebleeds"],
    "aspirin": ["GI_irritation", "stomach_ulcer", "bleeding_risk"],
    "ibuprofen": ["GI_irritation", "kidney_risk", "raised_blood_pressure"],
    "paracetamol": ["liver_toxicity_in_overdose"],
    "metformin": ["nausea", "diarrhea", "lactic_acidosis_rare"],
    "amoxicillin": ["diarrhea", "rash", "allergic_reaction"],
    "ciprofloxacin": ["tendon_rupture_risk", "nausea", "photosensitivity"],
    "omeprazole": ["headache", "diarrhea", "low_magnesium_long_term"],
    "atorvastatin": ["muscle_pain", "liver_enzyme_rise"],
    "simvastatin": ["muscle_pain", "rhabdomyolysis_rare"],
    "amlodipine": ["ankle_swelling", "flushing", "headache"],
    "lisinopril": ["dry_cough", "dizziness", "hyperkalemia"],
    "metoprolol": ["fatigue", "bradycardia", "cold_extremities"],
    "diazepam": ["sedation", "dependence_risk", "respiratory_depression"],
    "tramadol": ["nausea", "dizziness", "constipation", "seizure_risk"],
    "prednisone": ["weight_gain", "osteoporosis", "raised_blood_sugar", "immunosuppression"],
    "sertraline": ["nausea", "insomnia", "sexual_dysfunction"],
    "fluoxetine": ["nausea", "insomnia", "agitation"],
    "digoxin": ["nausea", "visual_disturbances", "arrhythmia_in_overdose"],
    "metronidazole": ["metallic_taste", "nausea", "alcohol_intolerance"],
}
