import json
from pathlib import Path

# --- FOOD DATA ---
food_safe = [
  {"item_id": "FOOD_001", "category": "Food", "product_name": "Basmati Rice", "ingredients": ["Basmati Rice"], "overall_health_status": "SAFE"},
  {"item_id": "FOOD_002", "category": "Food", "product_name": "Whole Wheat Flour", "ingredients": ["Whole Wheat"], "overall_health_status": "SAFE"},
  {"item_id": "FOOD_003", "category": "Food", "product_name": "Toor Dal", "ingredients": ["Pigeon Peas"], "overall_health_status": "SAFE"},
  {"item_id": "FOOD_004", "category": "Food", "product_name": "Moong Dal", "ingredients": ["Green Gram"], "overall_health_status": "SAFE"},
  {"item_id": "FOOD_005", "category": "Food", "product_name": "Rolled Oats", "ingredients": ["Whole Grain Oats"], "overall_health_status": "SAFE"},
  {"item_id": "FOOD_006", "category": "Food", "product_name": "Peanut Butter", "ingredients": ["Peanuts", "Salt"], "overall_health_status": "SAFE"},
  {"item_id": "FOOD_007", "category": "Food", "product_name": "Honey", "ingredients": ["Pure Honey"], "overall_health_status": "SAFE"},
  {"item_id": "FOOD_008", "category": "Food", "product_name": "Mustard Oil", "ingredients": ["Mustard Seed Oil"], "overall_health_status": "SAFE"}
]

food_banned = [
  {"item_id": "FOOD_B01", "category": "FOOD", "product_name": "Bakery Bread", "detected_substance": "Potassium Bromate", "status": "PROHIBITED", "reason": "Carcinogenic additive banned in bakery products", "authority": "FSSAI"},
  {"item_id": "FOOD_B02", "category": "FOOD", "product_name": "Artificially Ripened Mangoes", "detected_substance": "Calcium Carbide", "status": "PROHIBITED", "reason": "Prohibited acetylene gas emission during ripening", "authority": "FSSAI"},
  {"item_id": "FOOD_B03", "category": "FOOD", "product_name": "Yellow Besan", "detected_substance": "Metanil Yellow", "status": "PROHIBITED", "reason": "Non-permitted synthetic industrial dye", "authority": "FSSAI"},
  {"item_id": "FOOD_B04", "category": "FOOD", "product_name": "Pink Cotton Candy", "detected_substance": "Rhodamine B", "status": "PROHIBITED", "reason": "Prohibited industrial textile dye", "authority": "FSSAI"},
  {"item_id": "FOOD_B05", "category": "FOOD", "product_name": "Red Chilli Powder", "detected_substance": "Sudan I", "status": "PROHIBITED", "reason": "Genotoxic carcinogenic dye prohibited in spices", "authority": "FSSAI"}
]

# --- MEDICINE DATA ---
med_safe = [
  {"item_id": "MED_001", "category": "Medicine", "product_name": "Paracetamol Tablet", "active_ingredient": "Paracetamol", "overall_health_status": "SAFE"},
  {"item_id": "MED_002", "category": "Medicine", "product_name": "Cetirizine Syrup", "active_ingredient": "Cetirizine Hydrochloride", "overall_health_status": "SAFE"},
  {"item_id": "MED_003", "category": "Medicine", "product_name": "Oral Rehydration Formula", "active_ingredient": "Oral Rehydration Salts", "overall_health_status": "SAFE"},
  {"item_id": "MED_004", "category": "Medicine", "product_name": "Ibuprofen Capsule", "active_ingredient": "Ibuprofen", "overall_health_status": "SAFE"},
  {"item_id": "MED_005", "category": "Medicine", "product_name": "Omeprazole Delayed-Release", "active_ingredient": "Omeprazole", "overall_health_status": "SAFE"},
  {"item_id": "MED_006", "category": "Medicine", "product_name": "Antiseptic Wash", "active_ingredient": "Povidone Iodine", "overall_health_status": "SAFE"}
]

med_banned = [
  {"item_id": "MED_B01", "category": "MEDICINE", "product_name": "Amidopyrine Analgesic", "detected_substance": "Amidopyrine", "status": "PROHIBITED", "reason": "Severe agranulocytosis and bone marrow toxicity", "authority": "CDSCO"},
  {"item_id": "MED_B02", "category": "MEDICINE", "product_name": "Phenacetin Powder", "detected_substance": "Phenacetin", "status": "PROHIBITED", "reason": "Nephrotoxicity and urothelial carcinoma risks", "authority": "CDSCO"},
  {"item_id": "MED_B03", "category": "MEDICINE", "product_name": "Cisapride Suspension", "detected_substance": "Cisapride", "status": "PROHIBITED", "reason": "QT-prolongation and fatal cardiac arrhythmias", "authority": "CDSCO"},
  {"item_id": "MED_B04", "category": "MEDICINE", "product_name": "Pediatric Nimesulide Drops", "detected_substance": "Nimesulide", "status": "RESTRICTED", "reason": "Restricted in children below 12 due to fatal hepatotoxicity", "authority": "CDSCO"},
  {"item_id": "MED_B05", "category": "MEDICINE", "product_name": "Unapproved FDC", "detected_substance": "Cefuroxime + Serratiopeptidase", "status": "PROHIBITED_FDC", "reason": "Prohibited fixed-dose combination without therapeutic justification", "authority": "CDSCO"}
]

# --- COSMETICS DATA ---
cosmetics_safe = [
  {"item_id": "COS_001", "category": "Cosmetics", "product_name": "Hydrating Face Wash", "ingredients": ["Aqua", "Glycerin", "Cocamidopropyl Betaine", "Sodium Chloride"], "overall_health_status": "SAFE"},
  {"item_id": "COS_002", "category": "Cosmetics", "product_name": "Moisturizing Cream", "ingredients": ["Aqua", "Cetyl Alcohol", "Shea Butter", "Dimethicone", "Tocopherol"], "overall_health_status": "SAFE"},
  {"item_id": "COS_003", "category": "Cosmetics", "product_name": "Mineral Sunscreen", "ingredients": ["Zinc Oxide", "Caprylic Triglyceride", "Silica", "Glycerin"], "overall_health_status": "SAFE"},
  {"item_id": "COS_004", "category": "Cosmetics", "product_name": "Herbal Shampoo", "ingredients": ["Aqua", "Sodium Laureth Sulfate", "Amla Extract", "Aloe Barbadensis"], "overall_health_status": "SAFE"},
  {"item_id": "COS_005", "category": "Cosmetics", "product_name": "Niacinamide Serum", "ingredients": ["Aqua", "Niacinamide", "Zinc PCA", "Phenoxyethanol"], "overall_health_status": "SAFE"}
]

cosmetics_banned = [
  {"item_id": "COS_B01", "category": "COSMETICS", "product_name": "Fairness Bleach Cream", "detected_substance": "Mercury", "status": "PROHIBITED", "reason": "Neurotoxic heavy metal prohibited under BIS IS 4707 Part 1", "authority": "CDSCO"},
  {"item_id": "COS_B02", "category": "COSMETICS", "product_name": "Antimicrobial Medicated Soap", "detected_substance": "Bithionol", "status": "PROHIBITED", "reason": "Photocontact sensitizer prohibited in topical formulations", "authority": "CDSCO"},
  {"item_id": "COS_B03", "category": "COSMETICS", "product_name": "Rapid Skin Peeling Oil", "detected_substance": "Chloroform", "status": "PROHIBITED", "reason": "Prohibited hazardous solvent under Drugs and Cosmetics Rules", "authority": "BIS"},
  {"item_id": "COS_B04", "category": "COSMETICS", "product_name": "Depilatory Lotion", "detected_substance": "Hexachlorophene", "status": "PROHIBITED", "reason": "Banned neurotoxic bacteriostatic agent", "authority": "CDSCO"}
]

# --- AGRICULTURE DATA ---
agri_safe = [
  {"item_id": "AGR_001", "category": "Agriculture", "product_name": "Neem Oil Insecticide", "ingredients": ["Cold Pressed Neem Seed Oil", "Azadirachtin", "Polysorbate 20"], "overall_health_status": "SAFE"},
  {"item_id": "AGR_002", "category": "Agriculture", "product_name": "Organic Bio-Fertilizer", "ingredients": ["Rhizobium Culture", "Carrier Peat Powder"], "overall_health_status": "SAFE"},
  {"item_id": "AGR_003", "category": "Agriculture", "product_name": "Potash Enriched Fertilizer", "ingredients": ["Muriate of Potash", "Potassium Chloride"], "overall_health_status": "SAFE"},
  {"item_id": "AGR_004", "category": "Agriculture", "product_name": "Chelated Zinc Foliar Spray", "ingredients": ["Zinc EDTA", "Inert Surfactants"], "overall_health_status": "SAFE"},
  {"item_id": "AGR_005", "category": "Agriculture", "product_name": "Vermicompost Base", "ingredients": ["Decomposed Organic Matter", "Humic Acid"], "overall_health_status": "SAFE"}
]

agri_banned = [
  {"item_id": "AGR_B01", "category": "AGRICULTURE", "product_name": "Crop Spray EC", "detected_substance": "Endosulfan", "status": "PROHIBITED", "reason": "Complete statutory ban under Supreme Court & Insecticides Act 1968", "authority": "CIBRC"},
  {"item_id": "AGR_B02", "category": "AGRICULTURE", "product_name": "Vegetable Pest Powder", "detected_substance": "Monocrotophos", "status": "RESTRICTED", "reason": "Prohibited for use on vegetables due to high acute oral toxicity", "authority": "CIBRC"},
  {"item_id": "AGR_B03", "category": "AGRICULTURE", "product_name": "Grain Storage Fumigant", "detected_substance": "Aluminium Phosphide", "status": "RESTRICTED", "reason": "Strictly restricted to licensed government operators; toxic phosphine gas", "authority": "CIBRC"},
  {"item_id": "AGR_B04", "category": "AGRICULTURE", "product_name": "Weed Defoliator 24D", "detected_substance": "Diazinon", "status": "PROHIBITED", "reason": "Phased-out organophosphate with unacceptable ecological risk", "authority": "CIBRC"}
]

master = (
    food_safe + food_banned +
    med_safe + med_banned +
    cosmetics_safe + cosmetics_banned +
    agri_safe + agri_banned
)

raw_dir = Path("data/raw")
raw_dir.mkdir(parents=True, exist_ok=True)
target_path = raw_dir / "master_products.json"

with open(target_path, "w", encoding="utf-8") as f:
    json.dump(master, f, indent=2)

print(f"Dataset updated at: {target_path.resolve()}")
print(f"Total multi-sector products: {len(master)}")