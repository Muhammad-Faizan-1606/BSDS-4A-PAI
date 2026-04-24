"""
PrescriScan AI - Flask Backend
AI Prescription Reader & Medicine Interaction Checker
University Project - Data Science
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import json
import os
from ocr import extract_prescription_data
from prolog_engine import PrologEngine

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)  # Allow frontend to call this API

# Initialize Prolog engine on startup
prolog = PrologEngine(kb_path="../knowledge_base/drug_interactions.pl")

@app.route("/", methods=["GET"])
def index():
    return app.send_static_file('index.html')

@app.route("/api/info", methods=["GET"])
def api_info():
    return jsonify({
        "app": "PrescriScan AI",
        "version": "1.0.0",
        "status": "running",
        "endpoints": ["/analyze", "/interactions", "/dosage-check", "/side-effects", "/health"]
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "prolog": prolog.is_ready()})

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Main endpoint: accepts prescription image, returns full analysis.
    
    Request body (JSON):
      - image_base64: base64-encoded image string
      - image_type: "jpeg" | "png" | "pdf"  (default: jpeg)
    
    Returns:
      - ocr_text: raw extracted text
      - medicines: list of detected medicines with doses
      - interactions: drug interaction results from Prolog
      - dosage_checks: dosage validation results
      - side_effects: known side effects
      - safety_score: 0-100
      - overall_risk: Low | Moderate | High
      - summary: plain English summary
    """
    data = request.get_json()
    if not data or "image_base64" not in data:
        return jsonify({"error": "Missing image_base64 in request body"}), 400

    image_b64 = data["image_base64"]
    image_type = data.get("image_type", "jpeg")

    # Step 1: OCR - Extract text and medicines from image using Claude Vision
    try:
        ocr_result = extract_prescription_data(image_b64, image_type)
    except Exception as e:
        return jsonify({"error": f"OCR failed: {str(e)}"}), 500

    medicines = ocr_result.get("medicines", [])
    med_names = [m["name"].lower() for m in medicines]

    # Step 2: Query Prolog for drug interactions
    interactions = prolog.check_interactions(med_names)

    # Step 3: Validate dosages against Prolog knowledge base
    dosage_checks = prolog.check_dosages(medicines)

    # Step 4: Get side effects from Prolog
    side_effects = prolog.get_side_effects(med_names)

    # Step 5: Calculate safety score
    safety_score, overall_risk = calculate_risk(interactions, dosage_checks)

    return jsonify({
        "ocr_text": ocr_result.get("ocr_text", ""),
        "medicines": medicines,
        "interactions": interactions,
        "dosage_checks": dosage_checks,
        "side_effects": side_effects,
        "safety_score": safety_score,
        "overall_risk": overall_risk,
        "summary": ocr_result.get("summary", "")
    })


@app.route("/interactions", methods=["POST"])
def check_interactions():
    """
    Check interactions between a specific list of drug names.
    
    Request body: {"medicines": ["warfarin", "aspirin", "metformin"]}
    """
    data = request.get_json()
    medicines = data.get("medicines", [])
    if not medicines:
        return jsonify({"error": "No medicines provided"}), 400

    results = prolog.check_interactions([m.lower() for m in medicines])
    return jsonify({"interactions": results})


@app.route("/dosage-check", methods=["POST"])
def dosage_check():
    """
    Validate dosages for given medicines.
    
    Request body: {"medicines": [{"name": "paracetamol", "dose": "500mg", "frequency": "4x daily"}]}
    """
    data = request.get_json()
    medicines = data.get("medicines", [])
    results = prolog.check_dosages(medicines)
    return jsonify({"dosage_checks": results})


@app.route("/side-effects", methods=["POST"])
def side_effects():
    """Get known side effects for a list of drugs."""
    data = request.get_json()
    medicines = data.get("medicines", [])
    results = prolog.get_side_effects([m.lower() for m in medicines])
    return jsonify({"side_effects": results})


def calculate_risk(interactions, dosage_checks):
    """
    Calculate overall safety score (0-100) and risk level.
    Deduct points for dangerous interactions and bad dosages.
    """
    score = 100

    for interaction in interactions:
        severity = interaction.get("severity", "ok")
        if severity == "danger":
            score -= 30
        elif severity == "warning":
            score -= 10

    for check in dosage_checks:
        status = check.get("status", "ok")
        if status == "danger":
            score -= 25
        elif status == "warning":
            score -= 10

    score = max(0, score)

    if score >= 80:
        risk = "Low"
    elif score >= 55:
        risk = "Moderate"
    else:
        risk = "High"

    return score, risk


if __name__ == "__main__":
    print("Starting PrescriScan AI Backend...")
    print("API running at http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
