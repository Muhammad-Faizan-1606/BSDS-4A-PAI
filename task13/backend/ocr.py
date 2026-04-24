"""
ocr.py - Prescription OCR using Claude Vision API
Extracts medicine names, dosages, and patient info from prescription images.
"""

import google.generativeai as genai
import json
import re
import os


def extract_prescription_data(image_base64: str, image_type: str = "jpeg") -> dict:
    """
    Send prescription image to Google Gemini Vision API.
    Returns structured JSON with detected medicines and metadata.
    
    Args:
        image_base64: base64 encoded image string
        image_type: "jpeg", "png", or "gif"
    
    Returns:
        dict with keys: ocr_text, medicines, summary
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)

    prompt = """You are a medical AI assistant specialized in reading handwritten prescriptions.

Analyze this prescription image and extract all information.

Return ONLY valid JSON in this exact format (no markdown, no extra text):
{
  "ocr_text": "the complete raw text you can read from the prescription",
  "patient_name": "patient name if visible",
  "doctor_name": "doctor name if visible",
  "date": "prescription date if visible",
  "medicines": [
    {
      "name": "Medicine Name",
      "dose": "500mg",
      "frequency": "twice daily",
      "duration": "7 days",
      "route": "oral"
    }
  ],
  "summary": "One or two sentence plain English summary of this prescription"
}

Rules:
- Include ALL medicines you can detect, even if partially legible
- Normalize medicine names (e.g. "Tab. Paracetamol" → "Paracetamol")
- If you cannot read a value clearly, write "unclear"
- Never hallucinate medicines not visible in the image
- Return only the JSON object, nothing else"""

    media_type_map = {
        "jpeg": "image/jpeg",
        "jpg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp"
    }
    media_type = media_type_map.get(image_type.lower(), "image/jpeg")

    # For Google Generative AI we need to pass a dict with mime_type and base64 encoded data
    image_part = {
        "mime_type": media_type,
        "data": image_base64
    }

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    response = model.generate_content([prompt, image_part])

    raw_text = response.text.strip()

    # Strip markdown fences if model wrapped response
    raw_text = re.sub(r"^```json\s*", "", raw_text, flags=re.IGNORECASE)
    raw_text = re.sub(r"\s*```$", "", raw_text)

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback: return minimal structure if JSON parsing fails
        result = {
            "ocr_text": raw_text,
            "medicines": [],
            "summary": "Could not parse structured data from image."
        }

    return result


def normalize_medicine_name(name: str) -> str:
    """
    Clean up medicine names extracted from OCR.
    Removes prefixes like Tab., Cap., Inj., Syp.
    """
    prefixes = ["tab.", "cap.", "inj.", "syp.", "oint.", "drops", "tab", "cap"]
    name_lower = name.lower().strip()
    for prefix in prefixes:
        if name_lower.startswith(prefix):
            name = name[len(prefix):].strip()
            break
    return name.strip().title()


def parse_dose_mg(dose_str: str) -> float:
    """
    Parse dose string to numeric mg value for Prolog dosage checking.
    E.g. "500mg" -> 500.0, "1g" -> 1000.0
    """
    if not dose_str:
        return 0.0

    dose_str = dose_str.lower().strip()
    match_mg = re.search(r"([\d.]+)\s*mg", dose_str)
    match_g = re.search(r"([\d.]+)\s*g\b", dose_str)
    match_mcg = re.search(r"([\d.]+)\s*mcg", dose_str)

    if match_mg:
        return float(match_mg.group(1))
    elif match_g:
        return float(match_g.group(1)) * 1000
    elif match_mcg:
        return float(match_mcg.group(1)) / 1000

    return 0.0


def parse_frequency_per_day(freq_str: str) -> int:
    """
    Convert frequency string to times-per-day integer.
    E.g. "twice daily" -> 2, "three times a day" -> 3, "TDS" -> 3
    """
    if not freq_str:
        return 1

    freq_lower = freq_str.lower()

    mappings = {
        "once": 1, "od": 1, "daily": 1, "qd": 1,
        "twice": 2, "bd": 2, "bid": 2, "two times": 2,
        "three": 3, "tds": 3, "tid": 3, "thrice": 3,
        "four": 4, "qds": 4, "qid": 4,
        "six": 6, "six times": 6
    }

    for key, value in mappings.items():
        if key in freq_lower:
            return value

    return 1  # Default: assume once daily
