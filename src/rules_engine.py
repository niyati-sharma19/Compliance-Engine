import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
from src.preprocessor import ProductDatasetPreprocessor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "processed" / "standardized_products.csv"

class StatutoryRulesEngine:
    HEALTH_HAZARDS = [
        {
            "substance": "palm oil",
            "category": "FOOD",
            "authority": "FSSAI / WHO Health Advisory",
            "reason": "High Saturated Fat Hazard: Contains ~50% saturated palmitic acid. Significantly elevates LDL cholesterol, arterial plaque deposition, and coronary heart disease risk in fried snacks.",
            "severity": "HEALTH_HAZARD"
        },
        {
            "substance": "tbhq",
            "category": "FOOD",
            "authority": "FSSAI Food Additive Norms",
            "reason": "Synthetic phenolic antioxidant (INS 319); linked to cellular stress, liver strain, and biochemical toxicity at elevated consumption.",
            "severity": "HEALTH_HAZARD"
        },
        {
            "substance": "trans fat",
            "category": "FOOD",
            "authority": "FSSAI 2021 Regulation",
            "reason": "Strictly restricted under 2% cap: Industrial trans fatty acids cause coronary artery calcification and metabolic dysfunction.",
            "severity": "STATUTORY_BAN"
        }
    ]

    def __init__(self, processed_csv_path: Optional[str] = None):
        self.rules_db = []
        self.preprocessor = ProductDatasetPreprocessor()
        target_path = Path(processed_csv_path) if processed_csv_path else DEFAULT_CSV_PATH
        self._load_rules_from_dataset(str(target_path))
        # Add statutory health hazard definitions
        self.rules_db.extend(self.HEALTH_HAZARDS)

    def _load_rules_from_dataset(self, path: str):
        df = pd.read_csv(path)
        banned_df = df[df["is_banned"] == 1]
        
        for _, row in banned_df.iterrows():
            substance = str(row["clean_composition"]) if pd.notna(row["clean_composition"]) else ""
            if substance:
                self.rules_db.append({
                    "substance": substance,
                    "category": str(row["category"]).strip().upper(),
                    "authority": str(row["authority"]),
                    "reason": str(row["risk_reason"]),
                    "severity": "STATUTORY_BAN"
                })

    def evaluate(self, category: str, query_composition: str) -> Tuple[bool, List[Dict[str, str]]]:
        # Normalize text and expand additive codes (e.g. E924 -> potassium bromate, palmolein -> palm oil)
        normalized = self.preprocessor.normalize_text(query_composition)
        normalized_query = f" {normalized} "
        category = category.strip().upper()
        violations = []

        for rule in self.rules_db:
            if rule["category"] == category or rule["category"] == "ALL":
                substance_tokens = rule["substance"].split()
                # Check for exact pattern or token presence
                pattern = rf"\b{re.escape(rule['substance'])}\b"
                if re.search(pattern, normalized_query) or (
                    substance_tokens and all(f" {tok} " in normalized_query for tok in substance_tokens if len(tok) > 3)
                ):
                    display_name = "Palm Oil / Palmolein" if rule["substance"] == "palm oil" else rule["substance"].title()
                    violations.append({
                        "flagged_ingredient": display_name,
                        "regulator": rule["authority"],
                        "violation_reason": rule["reason"],
                        "severity": rule.get("severity", "STATUTORY_BAN")
                    })

        is_safe = len(violations) == 0
        return is_safe, violations