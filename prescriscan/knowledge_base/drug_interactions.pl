% ============================================================
% PrescriScan AI - Prolog Knowledge Base
% drug_interactions.pl
%
% Expert system for drug interaction detection,
% dosage validation, and side effect lookup.
%
% Run in SWI-Prolog: swipl -l drug_interactions.pl
% Query example:  ?- interacts(warfarin, aspirin, S, D).
% ============================================================

% ============================================================
% SECTION 1: Drug Interaction Facts
% Format: interacts(Drug1, Drug2, Severity, Description)
% Severity: danger | warning | ok
% ============================================================

interacts(warfarin, aspirin, danger,
    'Serious bleeding risk. Both drugs impair clotting — combined use greatly increases hemorrhage risk. Requires immediate physician review.').

interacts(warfarin, ibuprofen, danger,
    'NSAIDs potentiate warfarin anticoagulant effect significantly, raising risk of serious internal bleeding.').

interacts(ssri, maoi, danger,
    'Potentially fatal serotonin syndrome. These drug classes must NEVER be combined. Minimum 14-day washout required between them.').

interacts(maoi, tramadol, danger,
    'Risk of serotonin syndrome and seizures. Absolutely contraindicated. Do not combine under any circumstances.').

interacts(methotrexate, nsaid, danger,
    'NSAIDs reduce methotrexate clearance, causing toxic accumulation. Severe bone marrow suppression and renal failure possible.').

interacts(lithium, nsaid, danger,
    'NSAIDs reduce renal lithium clearance causing lithium toxicity. Can cause tremors, confusion, and cardiac arrhythmia.').

interacts(maoi, meperidine, danger,
    'Risk of fatal hyperpyrexia and hypertensive crisis. Absolutely contraindicated.').

interacts(cisapride, erythromycin, danger,
    'Both prolong QT interval — combination can cause fatal cardiac arrhythmia (Torsades de Pointes).').

interacts(clopidogrel, omeprazole, warning,
    'Omeprazole inhibits CYP2C19, reducing clopidogrel activation and potentially weakening its antiplatelet effect.').

interacts(digoxin, amiodarone, warning,
    'Amiodarone raises digoxin plasma level significantly. Digoxin dose reduction of 50% is usually required.').

interacts(amlodipine, simvastatin, warning,
    'Amlodipine inhibits simvastatin metabolism via CYP3A4, increasing risk of muscle toxicity (myopathy/rhabdomyolysis).').

interacts(ciprofloxacin, theophylline, warning,
    'Ciprofloxacin inhibits theophylline metabolism, raising plasma level and risk of theophylline toxicity.').

interacts(ace_inhibitor, potassium_supplement, warning,
    'ACE inhibitors reduce potassium excretion. Combined with supplements, serious hyperkalemia is possible.').

interacts(metformin, alcohol, warning,
    'Alcohol combined with metformin increases risk of lactic acidosis. Patient should avoid alcohol during treatment.').

interacts(warfarin, alcohol, warning,
    'Regular alcohol use increases warfarin anticoagulation effect unpredictably, raising bleeding risk.').

interacts(ssri, nsaid, warning,
    'SSRIs combined with NSAIDs increase risk of GI bleeding by inhibiting platelet aggregation and prostaglandin synthesis.').

interacts(fluoroquinolone, antacid, warning,
    'Antacids containing magnesium or aluminum chelate fluoroquinolones, drastically reducing absorption. Take 2 hours apart.').

% Symmetric rule: if A interacts with B, B interacts with A with same severity
interacts(Drug2, Drug1, Severity, Description) :-
    interacts(Drug1, Drug2, Severity, Description),
    Drug1 \= Drug2.


% ============================================================
% SECTION 2: Maximum Safe Daily Doses
% Format: max_dose(Drug, MaxDailyDose_in_mg)
% ============================================================

max_dose(paracetamol, 4000).
max_dose(acetaminophen, 4000).
max_dose(ibuprofen, 2400).
max_dose(aspirin, 4000).
max_dose(naproxen, 1500).
max_dose(warfarin, 15).
max_dose(metformin, 3000).
max_dose(amoxicillin, 3000).
max_dose(ciprofloxacin, 1500).
max_dose(azithromycin, 500).
max_dose(omeprazole, 80).
max_dose(pantoprazole, 80).
max_dose(atorvastatin, 80).
max_dose(simvastatin, 80).
max_dose(amlodipine, 10).
max_dose(lisinopril, 80).
max_dose(metoprolol, 400).
max_dose(losartan, 100).
max_dose(digoxin, 0.375).
max_dose(diazepam, 40).
max_dose(tramadol, 400).
max_dose(codeine, 240).
max_dose(morphine, 200).
max_dose(prednisone, 80).
max_dose(prednisolone, 80).
max_dose(dexamethasone, 40).
max_dose(cetirizine, 10).
max_dose(loratadine, 10).
max_dose(metronidazole, 2000).
max_dose(fluconazole, 400).
max_dose(sertraline, 200).
max_dose(fluoxetine, 80).
max_dose(escitalopram, 20).
max_dose(clonazepam, 20).
max_dose(alprazolam, 4).
max_dose(lithium, 2400).
max_dose(carbamazepine, 1600).
max_dose(phenytoin, 600).
max_dose(valproate, 2500).
max_dose(methotrexate, 30).   % oncology doses differ — this is for RA/psoriasis
max_dose(chloroquine, 500).
max_dose(hydroxychloroquine, 400).


% ============================================================
% SECTION 3: Side Effects
% Format: side_effect(Drug, Effect)
% Multiple facts per drug, one per effect
% ============================================================

side_effect(warfarin, bleeding_risk).
side_effect(warfarin, bruising).
side_effect(warfarin, nosebleeds).
side_effect(warfarin, hair_loss).

side_effect(aspirin, gi_irritation).
side_effect(aspirin, stomach_ulcer).
side_effect(aspirin, bleeding_risk).
side_effect(aspirin, tinnitus).

side_effect(ibuprofen, gi_irritation).
side_effect(ibuprofen, kidney_risk).
side_effect(ibuprofen, raised_blood_pressure).
side_effect(ibuprofen, fluid_retention).

side_effect(paracetamol, liver_toxicity_in_overdose).

side_effect(metformin, nausea).
side_effect(metformin, diarrhea).
side_effect(metformin, lactic_acidosis_rare).
side_effect(metformin, vitamin_b12_deficiency).

side_effect(amoxicillin, diarrhea).
side_effect(amoxicillin, rash).
side_effect(amoxicillin, allergic_reaction).
side_effect(amoxicillin, thrush).

side_effect(ciprofloxacin, tendon_rupture_risk).
side_effect(ciprofloxacin, nausea).
side_effect(ciprofloxacin, photosensitivity).
side_effect(ciprofloxacin, qt_prolongation).

side_effect(omeprazole, headache).
side_effect(omeprazole, diarrhea).
side_effect(omeprazole, low_magnesium_long_term).
side_effect(omeprazole, b12_deficiency_long_term).

side_effect(atorvastatin, muscle_pain).
side_effect(atorvastatin, liver_enzyme_rise).
side_effect(atorvastatin, rhabdomyolysis_rare).

side_effect(amlodipine, ankle_swelling).
side_effect(amlodipine, flushing).
side_effect(amlodipine, headache).
side_effect(amlodipine, palpitations).

side_effect(lisinopril, dry_cough).
side_effect(lisinopril, dizziness).
side_effect(lisinopril, hyperkalemia).
side_effect(lisinopril, angioedema_rare).

side_effect(metoprolol, fatigue).
side_effect(metoprolol, bradycardia).
side_effect(metoprolol, cold_extremities).
side_effect(metoprolol, depression).

side_effect(diazepam, sedation).
side_effect(diazepam, dependence_risk).
side_effect(diazepam, respiratory_depression).
side_effect(diazepam, memory_impairment).

side_effect(tramadol, nausea).
side_effect(tramadol, dizziness).
side_effect(tramadol, constipation).
side_effect(tramadol, seizure_risk).
side_effect(tramadol, dependence_risk).

side_effect(prednisone, weight_gain).
side_effect(prednisone, osteoporosis).
side_effect(prednisone, raised_blood_sugar).
side_effect(prednisone, immunosuppression).
side_effect(prednisone, insomnia).

side_effect(sertraline, nausea).
side_effect(sertraline, insomnia).
side_effect(sertraline, sexual_dysfunction).
side_effect(sertraline, weight_change).

side_effect(fluoxetine, nausea).
side_effect(fluoxetine, insomnia).
side_effect(fluoxetine, agitation).
side_effect(fluoxetine, sexual_dysfunction).

side_effect(digoxin, nausea).
side_effect(digoxin, visual_disturbances).
side_effect(digoxin, arrhythmia_in_overdose).
side_effect(digoxin, anorexia).

side_effect(metronidazole, metallic_taste).
side_effect(metronidazole, nausea).
side_effect(metronidazole, alcohol_intolerance).
side_effect(metronidazole, peripheral_neuropathy_long_term).


% ============================================================
% SECTION 4: Derived Rules
% Higher-level inferences built from base facts
% ============================================================

% Check if a drug is safe to prescribe (no dangerous interactions in a list)
safe_combination(DrugList) :-
    \+ (member(Drug1, DrugList),
        member(Drug2, DrugList),
        Drug1 \= Drug2,
        interacts(Drug1, Drug2, danger, _)).

% Collect all interactions for a drug pair
all_interactions(Drug1, Drug2, Interactions) :-
    findall(S-D, interacts(Drug1, Drug2, S, D), Interactions).

% Get all side effects for a drug as a list
all_side_effects(Drug, Effects) :-
    findall(E, side_effect(Drug, E), Effects).

% Validate that a dose is within safe range
valid_dose(Drug, DailyDoseMg) :-
    max_dose(Drug, MaxDose),
    DailyDoseMg =< MaxDose.

% Warn if dose is within 20% of maximum
near_max_dose(Drug, DailyDoseMg) :-
    max_dose(Drug, MaxDose),
    DailyDoseMg > MaxDose * 0.8,
    DailyDoseMg =< MaxDose.

% Flag overdose
exceeds_max_dose(Drug, DailyDoseMg) :-
    max_dose(Drug, MaxDose),
    DailyDoseMg > MaxDose.

% Danger level of an interaction
is_dangerous_interaction(Drug1, Drug2) :-
    interacts(Drug1, Drug2, danger, _).

is_moderate_interaction(Drug1, Drug2) :-
    interacts(Drug1, Drug2, warning, _).


% ============================================================
% SECTION 5: Utility Queries (for testing in SWI-Prolog REPL)
% ============================================================

% Example usage:
%   ?- interacts(warfarin, aspirin, S, D).
%   ?- max_dose(paracetamol, M).
%   ?- all_side_effects(metformin, E).
%   ?- safe_combination([metformin, omeprazole, amlodipine]).
%   ?- exceeds_max_dose(paracetamol, 5000).
%   ?- valid_dose(ibuprofen, 1200).
%   ?- findall(D, side_effect(warfarin, D), Effects).
