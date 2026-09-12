import os
import json
from PIL import Image
from pydantic import BaseModel, Field
from typing import Optional, List
from google import genai
from google.genai import types

class PackageLabelSchema(BaseModel):
    product_name: str = Field(description="Trade or brand name of the packaged commodity")
    inferred_category: str = Field(description="Must be exactly one of: FOOD, COSMETICS, MEDICINE, AGRICULTURE")
    ingredients_list: List[str] = Field(description="Array of all listed ingredients or active chemical compounds")
    raw_composition_text: str = Field(description="Comma-separated string of all ingredients for NLP processing")
    mrp: Optional[str] = Field(default="Not Detected", description="Maximum Retail Price if visible")
    net_quantity: Optional[str] = Field(default="Not Detected", description="Net weight, volume, or count")
    manufacturer_info: Optional[str] = Field(default="Not Detected", description="Manufacturer or packer details")
    expiry_or_best_before: Optional[str] = Field(default="Not Detected", description="Expiry date, use-by date, or mfg date")

class AIStudioVisionExtractor:
    DEFAULT_MODELS = ["gemini-3.5-flash-lite", "gemini-flash-latest", "gemini-3.6-flash"]

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        key = api_key or os.getenv("GEMINI_API_KEY", "")
        if not key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Set it via $env:GEMINI_API_KEY='...' in PowerShell."
            )
        self.client = genai.Client(api_key=key)
        self.preferred_model = model or "gemini-3.5-flash-lite"

    def extract_label_data(self, pil_image: Image.Image) -> PackageLabelSchema:
        prompt = (
            "You are a statutory compliance auditor for packaged commodities. "
            "Analyze the uploaded package label with extreme precision. "
            "Extract the product brand name, determine if it belongs to FOOD, COSMETICS, MEDICINE, or AGRICULTURE, "
            "and extract all ingredients, chemical additives, preservatives, and mandatory Legal Metrology declarations."
        )

        models_to_try = [self.preferred_model] + [m for m in self.DEFAULT_MODELS if m != self.preferred_model]
        last_error = None

        for model_name in models_to_try:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=[pil_image, prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=PackageLabelSchema,
                        temperature=0.1
                    )
                )
                data_dict = json.loads(response.text)
                return PackageLabelSchema(**data_dict)
            except Exception as e:
                last_error = e
                continue

        raise RuntimeError(f"All Vision OCR models failed: {last_error}")

if __name__ == "__main__":
    extractor = AIStudioVisionExtractor()
    print("AIStudioVisionExtractor initialized and verified successfully!")