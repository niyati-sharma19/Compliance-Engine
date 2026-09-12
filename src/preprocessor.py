import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW_PATH = PROJECT_ROOT / "data" / "raw" / "master_products.json"
DEFAULT_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

class ProductDatasetPreprocessor:
    # Standard mapping for common E/INS food codes to statutory names
    CODE_ALIASES = {
        "e924": "potassium bromate",
        "e924a": "potassium bromate",
        "e924b": "potassium iodate",
        "ins 924a": "potassium bromate",
        "e171": "titanium dioxide",
        "ins 171": "titanium dioxide",
        "e102": "tartrazine",
        "ins 102": "tartrazine",
        "e110": "sunset yellow",
        "e122": "carmoisine",
        "e127": "erythrosine",
        "e133": "brilliant blue",
        "palmolein": "palm oil",
        "palm olein": "palm oil",
        "fractionated palm oil": "palm oil",
        "edible vegetable oil palmolein": "palm oil",
        "edible vegetable oil palm oil": "palm oil",
        "ins 319": "tbhq",
        "ins 621": "monosodium glutamate",
        "msg": "monosodium glutamate",
        "partially hydrogenated oil": "trans fat"
    }

    def __init__(self, raw_data_path: Optional[str] = None):
        self.raw_data_path = Path(raw_data_path) if raw_data_path else DEFAULT_RAW_PATH

    def normalize_text(self, text: str) -> str:
        if not text or pd.isna(text):
            return ""
        
        # Convert to lower and normalize separators
        text = str(text).lower()
        
        # Replace aliases (e.g., E924 -> potassium bromate)
        for code, alias in self.CODE_ALIASES.items():
            pattern = rf"\b{re.escape(code)}\b"
            text = re.sub(pattern, alias, text)

        # Strip percentage markers and unnecessary noise (e.g., '35% ec', '(100%)')
        text = re.sub(r"\b\d+(\.\d+)?%\b", "", text)
        
        # Strip all punctuation except alphanumeric and space
        text = re.sub(r"[^\w\s]", " ", text)
        
        # Collapse multi-spaces
        return " ".join(text.split())

    def extract_composition(self, row: Dict[str, Any]) -> str:
        """Extracts composition from heterogeneous schema keys."""
        if "ingredients" in row and isinstance(row["ingredients"], list):
            return ", ".join(str(i) for i in row["ingredients"])
        if "active_ingredient" in row and row["active_ingredient"]:
            return str(row["active_ingredient"])
        if "detected_substance" in row and row["detected_substance"]:
            return str(row["detected_substance"])
        if "composition" in row and row["composition"]:
            return str(row["composition"])
        return ""

    def load_and_standardize(self) -> pd.DataFrame:
        if not self.raw_data_path.exists():
            raise FileNotFoundError(f"Missing master data file at: {self.raw_data_path}")

        with open(self.raw_data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        records = []
        for item in raw_data:
            composition = self.extract_composition(item)
            
            # Ground truth compliance logic
            status = str(item.get("status") or item.get("overall_health_status", "SAFE")).upper()
            is_banned = 1 if status in ["PROHIBITED", "RESTRICTED", "PROHIBITED_FDC", "BANNED", "CRITICAL"] else 0

            records.append({
                "item_id": item.get("item_id", "GEN_000"),
                "category": item.get("category", "UNKNOWN").strip().upper(),
                "product_name": item.get("product_name", "Unnamed Product"),
                "raw_composition": composition,
                "clean_composition": self.normalize_text(composition),
                "authority": item.get("authority", "NONE"),
                "risk_reason": item.get("reason", "No specific infraction noted."),
                "is_banned": is_banned
            })

        df = pd.DataFrame(records)
        DEFAULT_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(DEFAULT_PROCESSED_DIR / "standardized_products.csv", index=False)
        return df

if __name__ == "__main__":
    preprocessor = ProductDatasetPreprocessor()
    df = preprocessor.load_and_standardize()
    print("Pre-processing complete. Saved to data/processed/standardized_products.csv")
    print(f"Total entries: {len(df)}")
    print(df["is_banned"].value_counts())