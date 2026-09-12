# 🛡️ Enterprise Packaged Product Compliance & Regulatory Engine

An enterprise multi-tier statutory compliance verification and risk auditing engine for packaged commodities across **Food (FSSAI)**, **Cosmetics (CDSCO / BIS IS 4707)**, **Pharmaceuticals (CDSCO Section 26A)**, and **Agriculture (CIBRC / Insecticides Act 1968)**.

---

## 🚀 Key Features & Architecture

The compliance engine uses a multi-tier defense-in-depth architecture:

1. **Tier 1: Deterministic Statutory Rule Gate**
   - High-throughput regex pattern matching against statutory registers and gazette notifications.
   - Built-in **INS / E-Code additive expansion** (e.g. `E924` automatically resolves to carcinogenic `Potassium Bromate`).
   - Sector-specific statutory bodies: **FSSAI**, **CDSCO**, **BIS**, and **CIBRC**.

2. **Tier 2: Supervised ML & Explainable AI (XAI)**
   - Scikit-learn TF-IDF n-gram vectorizer paired with a Decision Tree Classifier.
   - Full explainability output: salient formulation tokens and transparent decision branch paths.
   - Calculates quantitative risk scores and actionable directives for quality assurance teams.

3. **Tier 3: Google Gemini Multimodal Vision Extractor**
   - Direct image scanning of packaged product back-panel labels.
   - Extracts trade name, category inference, full ingredients, chemical compounds, and Legal Metrology declarations (MRP, Net Quantity, Batch/Expiry, Manufacturer).

---

## 📁 Repository Structure

```text
Compliance_Engine/
├── api.py                    # FastAPI REST backend (/health, /api/v1/inspect, /api/v1/scan)
├── dashboard.py              # Interactive Streamlit audit workbench
├── pipeline.py               # EnterpriseComplianceEngine orchestrating Tier 1 & Tier 2
├── requirements.txt          # Python dependencies
├── .env.example              # Template environment configuration
├── .gitignore                # Git exclusions (bytecode, environments, logs)
├── data/
│   ├── raw/                  # Master product definitions and banned chemicals
│   └── processed/            # Standardized training datasets
├── models/
│   ├── compliance_tree_pipeline.pkl  # Serialized ML pipeline (TF-IDF + Decision Tree)
│   └── decision_tree_rules.txt       # Human-readable decision tree split rules
├── src/
│   ├── ai_studio_vision.py   # Gemini 3.6 Flash vision label extractor
│   ├── explain.py            # Decision path and salient token explainer
│   ├── preprocessor.py       # INS/E-code normalizer and dataset transformer
│   ├── report_generator.py   # Text-based compliance audit certificate generator
│   ├── rules_engine.py       # Statutory rules database engine
│   └── train.py              # Model training, evaluation, and rule export script
└── tests/
    └── test_engine.py        # Automated test suite
```

---

## ⚡ Quickstart & Installation

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Git

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/your-username/compliance-engine.git
cd compliance-engine

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key (Optional for Vision Scans)
If using the camera/label image scan features, configure your Google Gemini API key:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your_api_key_here"

# Linux / macOS
export GEMINI_API_KEY="your_api_key_here"
```
You can obtain an API key for free from [Google AI Studio](https://aistudio.google.com/).

---

## 🖥️ Running the Applications

### Interactive Streamlit Dashboard
Launch the visual audit workbench with preset samples and custom formulation testing:
```bash
streamlit run dashboard.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### FastAPI REST Server
Start the high-performance API:
```bash
uvicorn api:app --reload --port 8000
```
Interactive Swagger API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 📡 REST API Reference

### 1. Health Check
`GET /health`
```json
{
  "status": "ACTIVE",
  "engine_ready": true,
  "ai_studio_ready": true
}
```

### 2. Inspect Formulation
`POST /api/v1/inspect`
```json
{
  "category": "FOOD",
  "product_name": "Bakery Bread",
  "composition": "Wheat flour, yeast, E924, salt"
}
```
**Sample Response:**
```json
{
  "is_compliant": false,
  "status_badge": "NON-COMPLIANT / RECALL",
  "theme": "danger",
  "product_name": "Bakery Bread",
  "category": "FOOD",
  "risk_percentage": 100.0,
  "tier_triggered": "Tier 1: Statutory Authority Check",
  "summary": "Detected 1 statutory or toxicity infraction(s).",
  "action_directive": "Immediate product recall / formulation block.",
  "violations": [
    {
      "substance": "Potassium Bromate",
      "authority": "FSSAI",
      "hazard": "Carcinogenic flour improver banned under FSSAI 2016"
    }
  ]
}
```

### 3. Scan Package Label Image
`POST /api/v1/scan`
Multipart form upload with an image file (`image`) and optional `category` / `product_name`.

---

## 🧪 Testing & Model Retraining

### Run Automated Unit Tests
```bash
python -m unittest discover tests -v
```

### Retrain ML Decision Tree
```bash
# Preprocess master records
python src/preprocessor.py

# Retrain pipeline and export human-readable decision rules
python src/train.py
```

---

## ⚖️ License & Disclaimers
This software is intended for regulatory intelligence, automated screening, and compliance auditing workflows. Formal market clearance should always be confirmed against the latest official statutory gazettes published by designated national authorities.
