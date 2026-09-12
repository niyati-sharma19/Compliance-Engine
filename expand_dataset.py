import json
from pathlib import Path

# --- 1. FOOD DATASET (FSSAI) ---
food_records = [
    # Safe / Compliant
    {"category": "Food", "product_name": "Premium Whole Wheat Atta", "ingredients": ["Whole Wheat Grain"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Organic Brown Basmati", "ingredients": ["Brown Basmati Rice"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Cold Pressed Mustard Oil", "ingredients": ["Pure Mustard Seed Oil"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Roasted Peanuts Salted", "ingredients": ["Peanuts", "Iodized Salt"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Pure Desi Ghee", "ingredients": ["Milk Fat"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Multigrain Breakfast Flakes", "ingredients": ["Whole Oats", "Wheat Flakes", "Corn Grits", "Malt Extract"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Organic Turmeric Powder", "ingredients": ["Ground Turmeric Rhizome"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Natural Cane Jaggery", "ingredients": ["Sugarcane Juice Extract"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Green Tea Mint", "ingredients": ["Green Tea Leaves", "Dried Peppermint"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Almond Butter Creamy", "ingredients": ["Roasted California Almonds", "Sea Salt"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Sorghum Millet Crisps", "ingredients": ["Jowar Flour", "Sunflower Oil", "Cumin", "Salt"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Pure Raw Honey", "ingredients": ["Natural Forest Honey"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Kashmiri Chilli Powder", "ingredients": ["Dry Red Chillies"], "overall_health_status": "SAFE"},
    {"category": "Food", "product_name": "Unpolished Toor Dal", "ingredients": ["Pigeon Pea Splits"], "overall_health_status": "SAFE"},
    # Prohibited / Adulterated (FSSAI Violations)
    {"category": "FOOD", "product_name": "Super Soft Bakery Loaf", "detected_substance": "Potassium Bromate", "status": "PROHIBITED", "reason": "Carcinogenic flour improver banned under FSSAI 2016", "authority": "FSSAI"},
    {"category": "FOOD", "product_name": "Artificially Ripened Mangoes", "detected_substance": "Calcium Carbide", "status": "PROHIBITED", "reason": "Prohibited ripening chemical releasing toxic acetylene", "authority": "FSSAI"},
    {"category": "FOOD", "product_name": "Festive Besan Ladoo Mix", "detected_substance": "Metanil Yellow", "status": "PROHIBITED", "reason": "Banned non-permitted synthetic industrial dye", "authority": "FSSAI"},
    {"category": "FOOD", "product_name": "Bright Pink Fair Cotton Candy", "detected_substance": "Rhodamine B", "status": "PROHIBITED", "reason": "Banned toxic textile dye in foodstuffs", "authority": "FSSAI"},
    {"category": "FOOD", "product_name": "Export Red Chilli Powder", "detected_substance": "Sudan I", "status": "PROHIBITED", "reason": "Genotoxic carcinogenic industrial dye", "authority": "FSSAI"},
    {"category": "FOOD", "product_name": "Adulterated Mustard Oil", "detected_substance": "Argemone Oil", "status": "PROHIBITED", "reason": "Toxic sanguinarine adulterant causing epidemic dropsy", "authority": "FSSAI"},
    {"category": "FOOD", "product_name": "Polished Turmeric Root", "detected_substance": "Lead Chromate", "status": "PROHIBITED", "reason": "Neurotoxic heavy-metal pigment banned under FSS Act", "authority": "FSSAI"},
    {"category": "FOOD", "product_name": "Industrial Packaged Bread", "detected_substance": "Potassium Iodate", "status": "PROHIBITED", "reason": "Prohibited flour treatment agent", "authority": "FSSAI"}
]

# --- 2. COSMETICS DATASET (CDSCO / BIS IS 4707) ---
cosmetics_records = [
    # Safe / Compliant
    {"category": "Cosmetics", "product_name": "Deep Clean Face Wash", "ingredients": ["Aqua", "Cocamidopropyl Betaine", "Glycerin", "Sodium Chloride"], "overall_health_status": "SAFE"},
    {"category": "Cosmetics", "product_name": "Moisture Shield Body Lotion", "ingredients": ["Aqua", "Cetyl Alcohol", "Shea Butter", "Dimethicone", "Phenoxyethanol"], "overall_health_status": "SAFE"},
    {"category": "Cosmetics", "product_name": "Broad Spectrum Gel Sunscreen", "ingredients": ["Aqua", "Zinc Oxide", "Caprylic Triglyceride", "Silica", "Glycerin"], "overall_health_status": "SAFE"},
    {"category": "Cosmetics", "product_name": "Hyaluronic Hydrating Serum", "ingredients": ["Aqua", "Sodium Hyaluronate", "Propanediol", "Panthenol"], "overall_health_status": "SAFE"},
    {"category": "Cosmetics", "product_name": "Clarifying Tea Tree Shampoo", "ingredients": ["Aqua", "Sodium Laureth Sulfate", "Melaleuca Alternifolia Leaf Oil", "Citric Acid"], "overall_health_status": "SAFE"},
    {"category": "Cosmetics", "product_name": "Nourishing Hair Conditioner", "ingredients": ["Aqua", "Cetearyl Alcohol", "Argania Spinosa Kernel Oil", "Behentrimonium Chloride"], "overall_health_status": "SAFE"},
    {"category": "Cosmetics", "product_name": "Organic Lip Care Butter", "ingredients": ["Beeswax", "Cocos Nucifera Oil", "Castor Seed Oil", "Tocopherol"], "overall_health_status": "SAFE"},
    {"category": "Cosmetics", "product_name": "Exfoliating Walnut Face Scrub", "ingredients": ["Aqua", "Juglans Regia Shell Powder", "Stearic Acid", "Glycerin"], "overall_health_status": "SAFE"},
    {"category": "Cosmetics", "product_name": "Soothing Rosewater Toner", "ingredients": ["Rosa Damascena Flower Water", "Glycerin", "Sodium Benzoate"], "overall_health_status": "SAFE"},
    # Prohibited / Toxic (CDSCO & BIS Violations)
    {"category": "COSMETICS", "product_name": "Instant Fairness Bleaching Formula", "detected_substance": "Mercury", "status": "PROHIBITED", "reason": "Banned toxic heavy metal under BIS IS 4707 Part 1", "authority": "CDSCO"},
    {"category": "COSMETICS", "product_name": "Antimicrobial Hospital Soap", "detected_substance": "Bithionol", "status": "PROHIBITED", "reason": "Banned photocontact sensitizer in topical cosmetics", "authority": "CDSCO"},
    {"category": "COSMETICS", "product_name": "Chemical Skin Peel Solution", "detected_substance": "Chloroform", "status": "PROHIBITED", "reason": "Prohibited solvent under Drugs and Cosmetics Rules", "authority": "BIS"},
    {"category": "COSMETICS", "product_name": "Antiseptic Medicated Powder", "detected_substance": "Hexachlorophene", "status": "PROHIBITED", "reason": "Neurotoxic halogenated antibacterial prohibited in cosmetics", "authority": "CDSCO"},
    {"category": "COSMETICS", "product_name": "Kohl Eyeliner Traditional", "detected_substance": "Lead", "status": "PROHIBITED", "reason": "Prohibited heavy-metal contaminant in ocular cosmetics", "authority": "BIS"}
]

# --- 3. PHARMACEUTICAL / MEDICINE DATASET (CDSCO) ---
medicine_records = [
    # Safe / Approved Active Formulations
    {"category": "Medicine", "product_name": "Fever Relief Tablets", "active_ingredient": "Paracetamol", "overall_health_status": "SAFE"},
    {"category": "Medicine", "product_name": "Antiallergic Suspension", "active_ingredient": "Cetirizine Hydrochloride", "overall_health_status": "SAFE"},
    {"category": "Medicine", "product_name": "Electrolyte Rehydration Formula", "active_ingredient": "Oral Rehydration Salts", "overall_health_status": "SAFE"},
    {"category": "Medicine", "product_name": "NSAID Pain Reliever", "active_ingredient": "Ibuprofen", "overall_health_status": "SAFE"},
    {"category": "Medicine", "product_name": "Acid Reflux Capsule", "active_ingredient": "Omeprazole Delayed Release", "overall_health_status": "SAFE"},
    {"category": "Medicine", "product_name": "Topical Antiseptic Liquid", "active_ingredient": "Povidone Iodine Solution", "overall_health_status": "SAFE"},
    {"category": "Medicine", "product_name": "Cough Relief Expectorant", "active_ingredient": "Guaifenesin", "overall_health_status": "SAFE"},
    {"category": "Medicine", "product_name": "Antihypertensive Formulation", "active_ingredient": "Amlodipine Besylate", "overall_health_status": "SAFE"},
    {"category": "Medicine", "product_name": "Broad Spectrum Penicillin", "active_ingredient": "Amoxicillin Trihydrate", "overall_health_status": "SAFE"},
    # Banned / Restricted (CDSCO Section 26A Violations)
    {"category": "MEDICINE", "product_name": "Compound Analgesic Injection", "detected_substance": "Amidopyrine", "status": "PROHIBITED", "reason": "Severe agranulocytosis and fatal bone marrow toxicity", "authority": "CDSCO"},
    {"category": "MEDICINE", "product_name": "Headache Relief Powder", "detected_substance": "Phenacetin", "status": "PROHIBITED", "reason": "Nephrotoxicity and urinary tract carcinoma risk", "authority": "CDSCO"},
    {"category": "MEDICINE", "product_name": "Gastrointestinal Prokinetic Syrup", "detected_substance": "Cisapride", "status": "PROHIBITED", "reason": "Fatal ventricular arrhythmias and QT prolongation", "authority": "CDSCO"},
    {"category": "MEDICINE", "product_name": "Pediatric Fever Suspension 50mg", "detected_substance": "Nimesulide", "status": "RESTRICTED", "reason": "Banned in children below 12 years due to acute liver failure", "authority": "CDSCO"},
    {"category": "MEDICINE", "product_name": "Respiratory FDC Combination", "detected_substance": "Cefuroxime + Serratiopeptidase", "status": "PROHIBITED_FDC", "reason": "Prohibited irrational fixed-dose combination", "authority": "CDSCO"},
    {"category": "MEDICINE", "product_name": "Anti-obesity Appetite Suppressant", "detected_substance": "Sibutramine", "status": "PROHIBITED", "reason": "Excess cardiovascular events and stroke risk", "authority": "CDSCO"},
    {"category": "MEDICINE", "product_name": "Analgesic NSAID Tablet", "detected_substance": "Rofecoxib", "status": "PROHIBITED", "reason": "Severe thrombotic cardiovascular adverse events", "authority": "CDSCO"}
]

# --- 4. AGRICULTURE DATASET (CIBRC / INSECTICIDES ACT) ---
agri_records = [
    # Safe / Registered Bio-Inputs & Nutrients
    {"category": "Agriculture", "product_name": "Cold Pressed Neem Insecticide", "ingredients": ["Azadirachtin", "Neem Seed Oil"], "overall_health_status": "SAFE"},
    {"category": "Agriculture", "product_name": "Legume Bio-Fertilizer", "ingredients": ["Rhizobium Culture", "Carrier Peat"], "overall_health_status": "SAFE"},
    {"category": "Agriculture", "product_name": "Muriate of Potash 60%", "ingredients": ["Potassium Chloride"], "overall_health_status": "SAFE"},
    {"category": "Agriculture", "product_name": "Chelated Micronutrient Spray", "ingredients": ["Zinc EDTA", "Iron EDTA", "Surfactant"], "overall_health_status": "SAFE"},
    {"category": "Agriculture", "product_name": "Enriched Vermicompost", "ingredients": ["Organic Humus", "Decomposed Farmyard Residue"], "overall_health_status": "SAFE"},
    {"category": "Agriculture", "product_name": "Phosphate Solubilizing Bio-Inoculant", "ingredients": ["Bacillus megaterium Culture"], "overall_health_status": "SAFE"},
    {"category": "Agriculture", "product_name": "Sulfur Fertilizer 80% WDG", "ingredients": ["Dispersible Elemental Sulfur"], "overall_health_status": "SAFE"},
    {"category": "Agriculture", "product_name": "Trichoderma Viride Bio-Fungicide", "ingredients": ["Trichoderma Viride Spores", "Talc Carrier"], "overall_health_status": "SAFE"},
    # Prohibited / Restricted (CIBRC Statutory Bans)
    {"category": "AGRICULTURE", "product_name": "Crop Armor 35 EC", "detected_substance": "Endosulfan", "status": "PROHIBITED", "reason": "Statutory Supreme Court ban; persistent organic pollutant", "authority": "CIBRC"},
    {"category": "AGRICULTURE", "product_name": "Vegetable Protection Dust", "detected_substance": "Monocrotophos", "status": "RESTRICTED", "reason": "Prohibited for use on all vegetable crops (Class Ib acute toxin)", "authority": "CIBRC"},
    {"category": "AGRICULTURE", "product_name": "Stored Grain Fumigation Pellets", "detected_substance": "Aluminium Phosphide", "status": "RESTRICTED", "reason": "Restricted exclusively to authorized government operators", "authority": "CIBRC"},
    {"category": "AGRICULTURE", "product_name": "Broad Spectrum Orchard Insecticide", "detected_substance": "Diazinon", "status": "PROHIBITED", "reason": "Phased-out organophosphate insecticide", "authority": "CIBRC"},
    {"category": "AGRICULTURE", "product_name": "Total Weed Controller", "detected_substance": "Paraquat Dichloride", "status": "RESTRICTED", "reason": "Restricted high-toxicity herbicide; strict label claim limits", "authority": "CIBRC"}
]

# Consolidate and index records
all_records = food_records + cosmetics_records + medicine_records + agri_records

for idx, rec in enumerate(all_records, 1):
    rec["item_id"] = f"REG_{idx:03d}"

output_file = Path("data/raw/master_products.json")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_records, f, indent=2)

print(f"Dataset generated at: {output_file.resolve()}")
print(f"Total entries: {len(all_records)}")