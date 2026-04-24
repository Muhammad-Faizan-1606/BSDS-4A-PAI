---
title: PrescriScan AI
emoji: ⚕️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# PrescriScan AI
## AI Prescription Reader & Medicine Interaction Checker

> **University Project — BSc Data Science | Superior University, Lahore**
> 
> An AI-powered web application that uses computer vision to read handwritten medical prescriptions, converts them into structured digital text, and cross-checks prescribed medicines against a Prolog-based expert system to detect dangerous drug interactions, incorrect dosages, and potential side effects.

---

## Project Structure

```
prescriscan/
├── frontend/
│   └── index.html              ← Standalone web app (open directly in browser)
│
├── backend/
│   ├── app.py                  ← Flask API server (main entry point)
│   ├── ocr.py                  ← Claude Vision OCR module
│   ├── prolog_engine.py        ← SWI-Prolog bridge via pyswip
│   ├── drug_fallback.py        ← JSON fallback drug database
│   └── requirements.txt        ← Python dependencies
│
├── knowledge_base/
│   └── drug_interactions.pl    ← SWI-Prolog expert system
│
├── tests/
│   └── test_prolog_engine.py   ← Unit tests (pytest)
│
├── .env.example                ← Environment variable template
├── .gitignore
└── README.md
```

---

## Quick Start (Frontend Only — No Setup Needed)

1. Open `frontend/index.html` in any modern browser
2. Click **"Load Demo"** to see a sample prescription analysis
3. Upload your own prescription image to analyze it

> The frontend connects to the frontend mock demo directly from the browser (for demo purposes). In production, use the Flask backend.

---

## Full Setup (Backend + Prolog)

### Prerequisites
- Python 3.10+
- SWI-Prolog (for real Prolog queries)
- Gemini API key

### Install SWI-Prolog
```bash
# Ubuntu/Debian
sudo apt-get install swi-prolog

# macOS
brew install swi-prolog

# Windows
# Download from https://www.swi-prolog.org/Download.html
```

### Setup Python Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example ../.env
# Edit .env and add your GEMINI_API_KEY

# Run the server
python app.py
```

Server starts at: `http://localhost:5000`

### Connect Frontend to Backend
In `frontend/index.html`, change line:
```javascript
const USE_BACKEND = false;  // Change to: true
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and status |
| GET | `/health` | Health check including Prolog status |
| POST | `/analyze` | Full prescription analysis (main endpoint) |
| POST | `/interactions` | Check interactions for a drug list |
| POST | `/dosage-check` | Validate dosages |
| POST | `/side-effects` | Get side effects for drug list |

### Example: Analyze Prescription
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "<base64_encoded_image>",
    "image_type": "jpeg"
  }'
```

### Example: Check Interactions
```bash
curl -X POST http://localhost:5000/interactions \
  -H "Content-Type: application/json" \
  -d '{"medicines": ["warfarin", "aspirin", "metformin"]}'
```

---

## Prolog Knowledge Base

The expert system in `knowledge_base/drug_interactions.pl` contains:

- **Drug interaction facts** — severity-rated pairs (danger/warning/ok)
- **Maximum dose facts** — safe daily limits for 40+ drugs
- **Side effect facts** — known adverse effects per drug
- **Derived rules** — `valid_dose/2`, `safe_combination/1`, `exceeds_max_dose/2`

### Test in SWI-Prolog REPL
```prolog
swipl -l knowledge_base/drug_interactions.pl

?- interacts(warfarin, aspirin, S, D).
?- max_dose(paracetamol, M).
?- all_side_effects(metformin, Effects).
?- safe_combination([metformin, omeprazole, amlodipine]).
?- exceeds_max_dose(ibuprofen, 5000).
```

---

## How It Works

```
1. User uploads prescription image
         ↓
2. Google Gemini Vision API (OCR)
   → Reads handwritten text
   → Extracts: medicine names, doses, frequency
         ↓
3. Python Backend
   → Parses doses to numeric mg values
   → Generates all pairwise drug combinations
         ↓
4. Prolog Expert System
   → Queries: interacts(Drug1, Drug2, Severity, Description)
   → Queries: valid_dose(Drug, DailyDoseMg)
   → Queries: side_effect(Drug, Effect)
         ↓
5. Risk Calculator
   → Safety score: 100 - (30×dangers) - (10×warnings)
   → Risk level: Low / Moderate / High
         ↓
6. Results displayed in 5-tab UI
   → Overview, Interactions, Dosage, Side Effects, Raw OCR
```

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| AI / OCR | Google Gemini Vision API (Generative AI) |
| Backend | Python 3.10, Flask, Flask-CORS |
| Expert System | SWI-Prolog, pyswip (Python bridge) |
| Testing | pytest |

---

## Running Tests

```bash
cd prescriscan
python -m pytest tests/ -v
```

---

## Academic Context

This project demonstrates several core Computer Science and AI concepts:

- **Computer Vision / OCR** — Using multimodal AI to extract text from images
- **Expert Systems** — Rule-based inference engine in Prolog
- **Knowledge Representation** — Facts and rules in first-order logic
- **Natural Language Processing** — Parsing medical text into structured data
- **REST API Design** — Flask backend with clear endpoint architecture
- **Software Engineering** — Modular design, error handling, unit testing

---

## Disclaimer

This application is a **university prototype** for educational purposes only. It is NOT a substitute for professional medical advice. Always consult a licensed pharmacist or physician before making any medication decisions.

---

## Author

Muhammad Faizan | BSc Data Science | Superior University, Lahore  
LinkedIn: linkedin.com/in/muhammad-faizan-data-scientist
