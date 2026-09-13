import io 

from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from PIL import Image

from pipeline import EnterpriseComplianceEngine
from src.report_generator import ComplianceAuditReporter

# Import Google AI Studio extractor
try:
    from src.ai_studio_vision import AIStudioVisionExtractor
    vision_extractor = AIStudioVisionExtractor()
    ai_studio_ready = True
except Exception as e:
    vision_extractor = None
    ai_studio_ready = False
    print(f"Notice: Google AI Studio not initialized ({e}). Text inspection remains active.")

app = FastAPI(
    title="Packaged Product Compliance & Regulatory API",
    version="1.0.0",
    description="Multi-tier compliance engine for Food, Pharma/Cosmetics, and Agriculture"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = EnterpriseComplianceEngine()

def format_ui_response(result: Dict[str, Any], product_name: str, category: str, extracted_text: str = ""):
    is_safe = (result.get("overall_status") == "COMPLIANT")
    reasons = []

    if not is_safe:
        if "regulatory_citations" in result and result["regulatory_citations"]:
            for cit in result["regulatory_citations"]:
                reasons.append({
                    "substance": cit.get("flagged_ingredient", "Restricted Compound"),
                    "authority": cit.get("regulator", "Statutory Register"),
                    "hazard": cit.get("violation_reason", "Prohibited under statutory schedule.")
                })
        else:
            reasons.append({
                "substance": "High Toxicity Pattern",
                "authority": "Tier 2 ML Tree Classifier",
                "hazard": "Formulation composition triggered elevated risk thresholds."
            })

        is_hazard = (result.get("overall_status") == "HEALTH_HAZARD_WARNING")
        status_badge = "HEALTH HAZARD / WARNING" if is_hazard else "NON-COMPLIANT / RECALL"
        theme = "warning" if is_hazard else "danger"

        return {
            "is_compliant": False,
            "status_badge": status_badge,
            "theme": theme,
            "product_name": product_name,
            "category": category.upper(),
            "risk_percentage": round(result.get("risk_score", 1.0) * 100, 1),
            "tier_triggered": result.get("tier_triggered", "Statutory Rule Gate"),
            "summary": f"Detected {len(reasons)} statutory or health hazard infraction(s).",
            "action_directive": result.get("action_required", "Immediate regulatory block issued."),
            "violations": reasons,
            "raw_composition": extracted_text or result.get("clean_composition", "")
        }

    return {
        "is_compliant": True,
        "status_badge": "COMPLIANT / MARKET CLEARED",
        "theme": "success",
        "product_name": product_name,
        "category": category.upper(),
        "risk_percentage": round(result.get("risk_score", 0.0) * 100, 1),
        "tier_triggered": result.get("tier_triggered", "Tier 2: Cleared ML Threshold"),
        "summary": "Passed all statutory schedules and algorithmic toxicity checks.",
        "action_directive": "Product cleared for distribution and consumer purchase.",
        "violations": [],
        "raw_composition": extracted_text or result.get("clean_composition", "")
    }

class InspectionRequest(BaseModel):
    category: str = Field(..., examples=["FOOD"])
    product_name: str = Field(..., examples=["Enriched Bread"])
    composition: str = Field(..., examples=["Wheat flour, yeast, salt, potassium bromate"])

@app.get("/health")
def health_check():
    return {"status": "ACTIVE", "engine_ready": True, "ai_studio_ready": ai_studio_ready}

@app.post("/api/v1/inspect")
def inspect_single_product(payload: InspectionRequest):
    valid_categories = ["FOOD", "COSMETICS", "MEDICINE", "AGRICULTURE"]
    if payload.category.upper() not in valid_categories:
        raise HTTPException(status_code=400, detail=f"Category must be one of: {valid_categories}")

    raw_result = engine.inspect(
        category=payload.category,
        product_name=payload.product_name,
        composition=payload.composition
    )
    return format_ui_response(raw_result, payload.product_name, payload.category, payload.composition)

@app.post("/api/v1/scan")
async def scan_and_audit(
    category: Optional[str] = Form(default=None),
    product_name: Optional[str] = Form(default="Scanned Commodity"),
    image: UploadFile = File(...)
):
    if not ai_studio_ready or vision_extractor is None:
        raise HTTPException(
            status_code=500,
            detail="Google AI Studio API key not set. Set GEMINI_API_KEY environment variable."
        )

    contents = await image.read()
    pil_image = Image.open(io.BytesIO(contents))

    try:
        extracted = vision_extractor.extract_label_data(pil_image)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI Studio Vision Error: {str(e)}")

    final_category = (category or extracted.inferred_category or "FOOD").strip().upper()
    final_product_name = product_name if product_name and product_name != "Scanned Commodity" else extracted.product_name
    composition_string = extracted.raw_composition_text or ", ".join(extracted.ingredients_list)

    if not composition_string.strip():
        return {
            "is_compliant": False,
            "status_badge": "UNREADABLE INGREDIENTS",
            "theme": "warning",
            "product_name": final_product_name,
            "category": final_category,
            "risk_percentage": 0.0,
            "tier_triggered": "Vision Ingestion",
            "summary": "Label image lacked legible ingredient information.",
            "action_directive": "Re-scan the ingredient / back-panel area clearly.",
            "violations": [],
            "raw_composition": "",
            "declarations": extracted.model_dump()
        }

    raw_result = engine.inspect(
        category=final_category,
        product_name=final_product_name,
        composition=composition_string
    )

    ui_payload = format_ui_response(raw_result, final_product_name, final_category, composition_string)
    ui_payload["declarations"] = {
        "mrp": extracted.mrp,
        "net_quantity": extracted.net_quantity,
        "manufacturer": extracted.manufacturer_info,
        "expiry": extracted.expiry_or_best_before
    }
    return ui_payload


class MLIngredientsRequest(BaseModel):
    ingredients: str

@app.post("/api/ml/check-ingredients")
def check_ingredients_ml(payload: MLIngredientsRequest):
    result = engine.inspect(
        category="FOOD",
        product_name="Scanned Formulation",
        composition=payload.ingredients
    )
    banned = []
    restricted = []
    if "regulatory_citations" in result and result["regulatory_citations"]:
        for cit in result["regulatory_citations"]:
            banned.append({
                "names": [cit.get("flagged_ingredient", "").lower()],
                "status": "BANNED",
                "confidence": 1.0,
                "hazard": cit.get("violation_reason", "Statutory violation detected."),
                "remedy": f"Banned under {cit.get('regulator', 'Regulatory Authority')}. Immediate formulation block issued."
            })
    return {
        "detectedBanned": banned,
        "detectedRestricted": restricted
    }

class ProductScanRequest(BaseModel):
    productId: Optional[str] = None
    composition: Optional[str] = None

@app.post("/api/scan")
def scan_product_endpoint(payload: ProductScanRequest):
    comp = payload.composition or "wheat flour, potassium bromate, salt"
    result = engine.inspect(category="FOOD", product_name=payload.productId or "Product", composition=comp)
    is_safe = (result.get("overall_status") == "COMPLIANT")
    return {
        "productId": payload.productId or "PROD-001",
        "status": "COMPLIANT" if is_safe else "WARNING",
        "is_compliant": is_safe,
        "risk_percentage": round(result.get("risk_score", 0.0) * 100, 1),
        "violations": result.get("regulatory_citations", []),
        "salt": "NORMAL",
        "sugar": "SAFE"
    }

# Mount frontend directory for SPA and static assets
frontend_dir = Path(__file__).resolve().parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    import time
    import socket

    port = 8000
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", port))
        s.close()
    except OSError:
        port = 8001

    def open_browser():
        time.sleep(1.2)
        webbrowser.open(f"http://localhost:{port}")

    threading.Thread(target=open_browser, daemon=True).start()
    print(f"[*] Server starting! Automatically opening browser at http://localhost:{port} ...")
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)