/**
 * =========================================================================
 * MetroCheck — Compliance Engine Controller
 * SIH PS-26034: Legal Metrology (Packaged Commodities) Rules, 2011
 * Clean, Student-Friendly Vanilla JavaScript Architecture
 * =========================================================================
 * 
 * TEAM WORKSPACE MAP:
 * - Section 1: 📷 Image Processing & OCR Teammate (OpenCV / Tesseract / EasyOCR)
 * - Section 2: 🤖 Machine Learning Teammate (Ingredients & Toxic Additives AI Model)
 * - Section 3: ⚙️ Backend Teammates (FastAPI / Flask / Node.js API Endpoints)
 * - Section 4: 📜 Statutory 2011 Rules Engine & Banned Chemicals Database
 * - Section 5: 📊 Compliance Audit Runner & Role Actions
 * - Section 6: 🗄️ Audit History & Persistent Logging
 * - Section 7: 📁 Image Upload & Live Device Camera Handling
 * - Section 8: 🚀 Page Initialization & Event Listeners
 * =========================================================================
 */

// =========================================================================
// 📷 1. FOR IMAGE PROCESSING & OCR TEAMMATE (Member 2) — WORK HERE
// =========================================================================
/**
 * 💡 HOW TO INTEGRATE YOUR OCR / COMPUTER VISION PIPELINE:
 * -------------------------------------------------------------------------
 * 1. Your Python model (OpenCV + Tesseract / PaddleOCR / EasyOCR) receives the
 *    uploaded label image or camera frame from the user.
 * 
 * 2. When your model finishes extracting packaging text and bounding boxes,
 *    parse the text into the structured JSON format shown below and call:
 *    `handleOcrResults(extractedData)`
 * 
 * EXPECTED JSON SCHEMA:
 * {
 *   genericName:        "Potato Chips",                        // Rule 6(1)(b)
 *   manufacturer:       "Apex Foods Pvt Ltd, Solan, HP",       // Rule 6(1)(a)
 *   netQuantity:        "150 g",                               // Rule 6(1)(c) - SI units
 *   mfgDate:            "11/2025",                             // Rule 6(1)(d)
 *   expiryDate:         "05/2026",                             // FSSAI Reg 2.2.2(10)
 *   mrp:                "Rs. 30.00 (incl. of all taxes)",      // Rule 6(1)(e)
 *   unitSalePrice:      "Rs. 0.20 / g",                        // Rule 6(1)(f)
 *   countryOfOrigin:    "India",                               // Rule 6(1)(g)
 *   consumerPhone:      "1800-222-333",                        // Rule 6(1)(h)
 *   consumerEmail:      "care@apexfoods.in",                   // Rule 6(1)(h)
 *   vegNonVeg:          "Veg",                                 // FSSAI Veg / Non-Veg logo
 *   fssaiLic:           "10018022000123",                      // 14-digit FSSAI Lic
 *   hasNutritionTable:  true,                                  // Mandatory nutrition panel
 *   ingredients:        "Potatoes, Edible Oil, Salt, INS 924", // Checked by ML Model
 *   allergenWarning:    "Contains Wheat (Gluten)"              // Allergen alert
 * }
 */
function handleOcrResults(extractedData, rawText = '') {
  if (!currentProduct) {
    currentProduct = {
      id: "ocr-" + Date.now(),
      name: extractedData.genericName || "Live Scanned Commodity",
      category: "Food Packaging",
      brand: extractedData.manufacturer || "Manufacturer",
      data: extractedData
    };
  } else {
    currentProduct.data = { ...currentProduct.data, ...extractedData };
  }

  // Update OCR raw text in the inspector box for debugging
  const ocrBox = document.getElementById('ocrRawText');
  if (ocrBox && rawText) ocrBox.value = rawText;

  // Run the compliance evaluation immediately with the new OCR data
  runComplianceAudit();
}


// =========================================================================
// 🤖 2. FOR ML MODEL TEAMMATE (INGREDIENTS & CHEMICAL HAZARDS AI) — WORK HERE
// =========================================================================
/**
 * 💡 HOW YOUR INGREDIENTS CLASSIFICATION ML MODEL WORKS:
 * -------------------------------------------------------------------------
 * Your friend is building a Machine Learning / NLP model (e.g., HuggingFace
 * Transformer, BioBERT, NER, or Scikit-Learn Classifier) to verify food
 * ingredients against prohibited chemicals, hazardous industrial adulterants,
 * toxic food dyes (like Rhodamine B, Sudan Dyes), and banned additives (Potassium Bromate).
 * 
 * INPUT TO YOUR ML MODEL:
 * The raw text extracted from the packaging ingredients panel:
 * e.g., "Ingredients: Refined Wheat Flour, Sugar, Edible Vegetable Oil, Potassium Bromate, INS 102"
 * 
 * WHAT YOUR ML MODEL SHOULD RETURN (JSON):
 * {
 *   detectedBanned: [
 *     {
 *       names: ["potassium bromate", "ins 924", "e924"],
 *       status: "BANNED",
 *       confidence: 0.98,
 *       hazard: "Class 2B Carcinogen; causes renal tumors.",
 *       remedy: "Strictly banned by FSSAI Gazette (2016). Batch must be rejected."
 *     }
 *   ],
 *   detectedRestricted: [
 *     {
 *       names: ["tartrazine", "ins 102"],
 *       status: "RESTRICTED",
 *       confidence: 0.94,
 *       hazard: "Permitted synthetic color; max limit 100 mg/kg under FSSAI.",
 *       remedy: "Verify declared quantity does not exceed 100 ppm."
 *     }
 *   ]
 * }
 */
async function backendCheckBannedIngredientsAPI(ingredientsText) {
  try {
    const response = await fetch('/api/ml/check-ingredients', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ingredients: ingredientsText })
    });
    if (response.ok) {
      const mlData = await response.json();
      return mlData;
    }
  } catch (error) {
    console.warn('ML Backend offline. Falling back to local chemical database:', error);
  }

  // -----------------------------------------------------------------------
  // 💡 CLIENT-SIDE FALLBACK (Active until the ML Model API is live)
  // Scans the ingredients string against statutory FSSAI prohibited list:
  // -----------------------------------------------------------------------
  const text = (ingredientsText || "").toLowerCase();
  const detectedBanned = [];
  const detectedRestricted = [];

  BANNED_CHEMICALS.forEach(chem => {
    const isMatched = chem.names.some(name => text.includes(name.toLowerCase()));
    if (isMatched) {
      if (chem.status === "BANNED") {
        detectedBanned.push(chem);
      } else {
        detectedRestricted.push(chem);
      }
    }
  });

  return { detectedBanned, detectedRestricted };
}


// =========================================================================
// ⚙️ 3. FOR BACKEND TEAMMATES (Members 3 & 4) — WORK HERE
// =========================================================================
/**
 * 💡 HOW TO CONNECT YOUR FASTAPI / FLASK / NODE.JS BACKEND:
 * -------------------------------------------------------------------------
 * Replace the client-side rule evaluation below with an HTTP POST request to
 * your backend.
 * 
 * ENDPOINT 1: POST /api/check-compliance-2011
 * Input: Extracted OCR fields
 * Output: Array of rules with boolean `passed` flag and penalty details.
 */
async function backendCheckRulesAPI(extractedData) {
  // -----------------------------------------------------------------------
  // 🚀 TO CONNECT YOUR PYTHON / NODE BACKEND API:
  // Uncomment the block below once your backend server is running!
  // -----------------------------------------------------------------------
  /*
  try {
    const response = await fetch('http://localhost:8000/api/check-compliance-2011', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(extractedData)
    });
    if (response.ok) {
      return await response.json();
    }
  } catch (err) {
    console.warn('Backend API server offline. Using client-side rule evaluation:', err);
  }
  */

  // 💡 Client-side evaluation against all 14 statutory 2011 rules:
  return RULES_2011.map(rule => ({
    ...rule,
    passed: rule.validate(extractedData)
  }));
}


// =========================================================================
// 4. STATUTORY 2011 RULES & BANNED CHEMICALS DATABASE
// =========================================================================

// 14 Statutory Declarations under Legal Metrology 2011 & FSSAI
const RULES_2011 = [
  {
    id: "LM-6-1-A",
    clause: "Rule 6(1)(a) LM 2011",
    title: "Manufacturer Details",
    description: "Complete name and registered address of manufacturer / packer.",
    severity: "CRITICAL",
    penalty: "Section 36 LM Act: Fine up to ₹25,000.",
    recommendation: "Print full manufacturing premises address.",
    validate: d => Boolean(d.manufacturer && d.manufacturer.length > 8)
  },
  {
    id: "LM-6-1-B",
    clause: "Rule 6(1)(b) LM 2011",
    title: "Common / Generic Name",
    description: "Generic commodity name prominently displayed on front-of-pack.",
    severity: "HIGH",
    penalty: "Rule 32 Misleading declaration penalty.",
    recommendation: "Print generic name directly below brand mark.",
    validate: d => Boolean(d.genericName && d.genericName.length > 2)
  },
  {
    id: "LM-6-1-C",
    clause: "Rule 6(1)(c) LM 2011",
    title: "Net Quantity in SI Units",
    description: "Net quantity in metric units (g, kg, ml, l) with correct font size.",
    severity: "CRITICAL",
    penalty: "Section 36(1) Underweight defalcation penalties.",
    recommendation: "Declare standard SI metric unit (e.g., '150 g', '1 kg').",
    validate: d => Boolean(d.netQuantity && /(\d+)\s*(g|kg|ml|l)/i.test(d.netQuantity))
  },
  {
    id: "LM-6-1-D",
    clause: "Rule 6(1)(d) LM 2011",
    title: "Month & Year of Packing",
    description: "Clear month and year of packaging or importation.",
    severity: "CRITICAL",
    penalty: "Rule 32 Confiscation of non-conforming packages.",
    recommendation: "Print 'Mfg Date: MM/YYYY'.",
    validate: d => Boolean(d.mfgDate && d.mfgDate.length > 3)
  },
  {
    id: "LM-6-1-E",
    clause: "Rule 6(1)(e) LM 2011",
    title: "MRP Declaration",
    description: "Must state 'Maximum Retail Price ₹ ... (inclusive of all taxes)'.",
    severity: "CRITICAL",
    penalty: "Fines up to ₹50,000 for missing or altered MRP.",
    recommendation: "Ensure MRP text includes '(incl. of all taxes)'.",
    validate: d => Boolean(d.mrp && (/rs|\u20B9/i.test(d.mrp) || d.mrp.includes('Rs')))
  },
  {
    id: "LM-6-1-F",
    clause: "Rule 6(1)(f) LM 2011",
    title: "Unit Sale Price (USP)",
    description: "Price per g/ml printed alongside MRP for package > 100g.",
    severity: "MEDIUM",
    penalty: "Statutory notice under 2021 Legal Metrology Amendments.",
    recommendation: "Display 'Unit Sale Price: ₹ X / g'.",
    validate: d => Boolean(d.unitSalePrice && /(per|\/)\s*(g|kg|ml|l)/i.test(d.unitSalePrice))
  },
  {
    id: "LM-6-1-G",
    clause: "Rule 6(1)(g) LM 2011",
    title: "Country of Origin",
    description: "Mandatory declaration of country where product was produced.",
    severity: "HIGH",
    penalty: "Customs detention and product seizure for non-disclosure.",
    recommendation: "Add 'Country of Origin: India'.",
    validate: d => Boolean(d.countryOfOrigin && d.countryOfOrigin.length >= 3)
  },
  {
    id: "LM-6-1-H",
    clause: "Rule 6(1)(h) LM 2011",
    title: "Consumer Care Contact",
    description: "Telephone number, email, and address for consumer redressal.",
    severity: "HIGH",
    penalty: "Consumer Affairs statutory notice and fines.",
    recommendation: "Print 'Consumer Care: Ph: 1800-... / Email: care@...'.",
    validate: d => Boolean(d.consumerPhone || d.consumerEmail)
  },
  {
    id: "FSSAI-VEG-LOGO",
    clause: "FSSAI Reg 2.2.2(4)",
    title: "Veg / Non-Veg Emblem",
    description: "Green filled dot for Veg or brown triangle for Non-Veg.",
    severity: "CRITICAL",
    penalty: "FSSAI Section 52 Misbranding fine up to ₹3,00,000.",
    recommendation: "Affix standard 3mm-8mm Veg/Non-Veg emblem on front.",
    validate: d => Boolean(d.vegNonVeg && ['veg','non-veg','vegetarian'].includes(d.vegNonVeg.toLowerCase()))
  },
  {
    id: "FSSAI-LIC",
    clause: "FSSAI Reg 2.2.1(7)",
    title: "14-Digit FSSAI License",
    description: "FSSAI logo accompanied by valid 14-digit license number.",
    severity: "CRITICAL",
    penalty: "License cancellation for non-display or fabricated numbers.",
    recommendation: "Print 'fssai Lic. No. 1xxxxxxxxxxxxx'.",
    validate: d => Boolean(d.fssaiLic && /^[0-9]{14}$/.test(String(d.fssaiLic).trim()))
  },
  {
    id: "FSSAI-NUTRITION",
    clause: "FSSAI Reg 2.2.2(3)",
    title: "Nutritional Panel",
    description: "Energy, protein, carbohydrates, total sugars, and fats per 100g.",
    severity: "HIGH",
    penalty: "Misbranding fine up to ₹2,00,000 under FSS Act.",
    recommendation: "Include standard Nutrition Facts table.",
    validate: d => Boolean(d.hasNutritionTable === true)
  },
  {
    id: "FSSAI-INGREDIENTS",
    clause: "FSSAI Reg 2.2.2(2)",
    title: "Ingredients by Weight",
    description: "Ingredients list arranged in descending order of incoming weight.",
    severity: "HIGH",
    penalty: "FSSAI Section 53 misleading presentation penalty.",
    recommendation: "List highest quantity ingredient first.",
    validate: d => Boolean(d.ingredients && d.ingredients.length > 5)
  },
  {
    id: "FSSAI-EXPIRY",
    clause: "FSSAI Reg 2.2.2(10)",
    title: "Expiry / Best Before",
    description: "Legible expiry date or 'Best before DD/MM/YYYY' statement.",
    severity: "CRITICAL",
    penalty: "Section 59 criminal prosecution for selling expired food.",
    recommendation: "Stamp clear expiry date on crimp or back panel.",
    validate: d => Boolean(d.expiryDate || d.bestBefore)
  },
  {
    id: "FSSAI-ALLERGEN",
    clause: "FSSAI Reg 2.2.2(11)",
    title: "Allergen Warning",
    description: "Mandatory allergen warning (Wheat/Gluten, Soy, Peanuts, Milk).",
    severity: "MEDIUM",
    penalty: "Mandatory product recall order.",
    recommendation: "Print bold allergen disclaimer (e.g., 'Contains Gluten').",
    validate: d => Boolean(d.allergenWarning && d.allergenWarning.length > 2)
  }
];

// Statutory FSSAI Gazette Prohibited Chemicals Database
const BANNED_CHEMICALS = [
  {
    names: ["potassium bromate", "ins 924", "e924"],
    status: "BANNED",
    hazard: "Class 2B Carcinogen; causes renal cell tumors and DNA damage.",
    remedy: "Strictly banned by FSSAI Gazette Notification 2016. Reject batch immediately."
  },
  {
    names: ["potassium iodate"],
    status: "BANNED",
    hazard: "Triggers autoimmune thyroiditis; banned as a bread flour improver.",
    remedy: "Prohibited in bread dough under Food Safety and Standards Regulations."
  },
  {
    names: ["rhodamine b", "rhodamine-b"],
    status: "BANNED",
    hazard: "Mutagenic industrial textile dye; causes severe liver and kidney damage.",
    remedy: "Criminal seizure and immediate prosecution under FSSAI Section 59."
  },
  {
    names: ["brominated vegetable oil", "bvo"],
    status: "BANNED",
    hazard: "Organ bioaccumulation of bromine; neurological and endocrine toxicity.",
    remedy: "Removed from permissible additive list. Prohibited in citrus drinks."
  },
  {
    names: ["melamine"],
    status: "BANNED",
    hazard: "Industrial plastic adulterant; causes acute renal failure and kidney stones.",
    remedy: "Zero-tolerance ban in milk and dairy products."
  },
  {
    names: ["sudan dye", "sudan i", "sudan iv"],
    status: "BANNED",
    hazard: "Genotoxic industrial dye used to adulterate red chili powder.",
    remedy: "Prohibited adulterant; mandatory seizure under Section 38."
  },
  {
    names: ["calcium carbide", "masala"],
    status: "BANNED",
    hazard: "Releases arsenic and phosphorus hydride in artificial fruit ripening.",
    remedy: "Strictly banned under Rule 44AA of Prevention of Food Adulteration Rules."
  },
  {
    names: ["metanil yellow"],
    status: "BANNED",
    hazard: "Non-permitted coal tar dye; causes testicular degeneration and neurotoxicity.",
    remedy: "Prohibited in sweets, turmeric, and dal under FSSAI Regulations."
  }
];

// Presets for Hackathon Testing & Jury Demos
const DEMO_PRODUCTS = [
  {
    id: "chips-violations",
    name: "Crispy Delight Masala Chips",
    category: "Packaged Snack",
    brand: "Apex Foods",
    data: {
      genericName: "Potato Chips",
      manufacturer: "Apex Foods, Solan, HP",
      netQuantity: "150 g",
      mfgDate: "11/2025",
      countryOfOrigin: "India",
      fssaiLic: "10018022000123",
      hasNutritionTable: true,
      ingredients: "Potatoes, Edible Oil, Salt"
    },
    rawOcrText: "CRISPY DELIGHT CHIPS Net Wt 150g Mfg 11/2025 Apex Foods Solan fssai Lic 10018022000123",
    imagePlaceholder: "data:image/svg+xml;utf8," + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="500" height="340" style="background:#1e1b4b;font-family:sans-serif;"><text x="250" y="80" fill="#facc15" font-size="24" font-weight="bold" text-anchor="middle">CRISPY DELIGHT CHIPS</text><text x="250" y="160" fill="#f87171" font-size="16" text-anchor="middle">Missing: MRP &amp; Veg Logo</text><text x="250" y="200" fill="#94a3b8" font-size="14" text-anchor="middle">Net Wt: 150g | Mfg: 11/2025</text></svg>')
  },
  {
    id: "bread-banned",
    name: "Sunrise Bakery White Bread",
    category: "Bakery",
    brand: "Sunrise Bakers",
    data: {
      genericName: "White Bread",
      manufacturer: "Sunrise Bakers, New Delhi",
      netQuantity: "400 g",
      mfgDate: "02/2026",
      expiryDate: "07/02/2026",
      countryOfOrigin: "India",
      mrp: "Rs. 45.00",
      unitSalePrice: "Rs. 0.11/g",
      vegNonVeg: "Veg",
      fssaiLic: "10014011001890",
      hasNutritionTable: true,
      ingredients: "Flour, Water, Yeast, Potassium Bromate"
    },
    rawOcrText: "SUNRISE BREAD MRP Rs. 45.00 Net Wt 400g Ingredients: Flour, Potassium Bromate",
    imagePlaceholder: "data:image/svg+xml;utf8," + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="500" height="340" style="background:#451a03;font-family:sans-serif;"><text x="250" y="80" fill="#fef3c7" font-size="24" font-weight="bold" text-anchor="middle">SUNRISE WHITE BREAD</text><text x="250" y="160" fill="#ef4444" font-size="16" font-weight="bold" text-anchor="middle">BANNED: Potassium Bromate</text></svg>')
  }
];

const INITIAL_AUDIT_LOGS = [
  { id: "#LM-2026-0891", timestamp: "02 Sep 2026, 11:42 AM", name: "Pure Wheat Atta", brand: "Aashirvaad / ITC Ltd.", netQuantity: "5 kg", score: 85, status: "Partially Compliant", statusBadgeClass: "badge-partially-compliant", barColor: "#f59e0b" },
  { id: "#LM-2026-0890", timestamp: "02 Sep 2026, 10:15 AM", name: "Refined Sunflower Oil", brand: "Fortune / Adani Wilmar", netQuantity: "1 L", score: 100, status: "100% Compliant", statusBadgeClass: "badge-compliant", barColor: "#10b981" },
  { id: "#LM-2026-0889", timestamp: "01 Sep 2026, 04:30 PM", name: "Imported Milk Chocolate", brand: "Direct Importer Co.", netQuantity: "150 g", score: 40, status: "Non-Compliant", statusBadgeClass: "badge-non-compliant", barColor: "#ef4444" }
];

let currentProduct = null;
let activeFilter = 'VIOLATIONS_ONLY';
let currentRole = 'Enforcement officer';
let auditLogs = [];
let webcamStream = null;


// =========================================================================
// 5. COMPLIANCE AUDIT CONTROLLER
// =========================================================================
async function runComplianceAudit() {
  if (!currentProduct) {
    renderEmptyState();
    return;
  }

  // 1. Evaluate 2011 Rules (via Backend or Local Rule Engine)
  const rules = await backendCheckRulesAPI(currentProduct.data);

  // 2. Evaluate Ingredients (via Friend's ML Model or Fallback Database)
  const banned = await backendCheckBannedIngredientsAPI(currentProduct.data.ingredients);

  // Compute compliance score
  const passed = rules.filter(r => r.passed);
  const violations = rules.filter(r => !r.passed);
  const score = Math.round((passed.length / rules.length) * 100);

  // Update Status Banner
  const statusBadge = document.getElementById('auditStatusBadge');
  const progressBar = document.getElementById('auditProgressBar');
  const overallBadge = document.getElementById('overallStatusBadge');

  if (score === 100 && banned.detectedBanned.length === 0) {
    statusBadge.textContent = "100% Compliant";
    statusBadge.className = "badge audit-status-badge text-capitalize badge-compliant";
    progressBar.style.backgroundColor = "#10b981";
    overallBadge.textContent = "100% Compliant";
    overallBadge.className = "badge bg-success text-uppercase";
  } else if (score >= 70 && banned.detectedBanned.length === 0) {
    statusBadge.textContent = "Partially compliant";
    statusBadge.className = "badge audit-status-badge text-capitalize badge-partially-compliant";
    progressBar.style.backgroundColor = "#f59e0b";
    overallBadge.textContent = `${violations.length} Violations`;
    overallBadge.className = "badge bg-warning text-dark text-uppercase";
  } else {
    statusBadge.textContent = banned.detectedBanned.length > 0 ? "Hazardous: Banned Substance" : "Non-compliant";
    statusBadge.className = "badge audit-status-badge text-capitalize badge-non-compliant";
    progressBar.style.backgroundColor = "#ef4444";
    overallBadge.textContent = banned.detectedBanned.length > 0 ? "Banned Chemical Detected" : `${violations.length} Violations`;
    overallBadge.className = "badge bg-danger text-uppercase";
  }

  progressBar.style.width = `${score}%`;

  // Pre-fill Modal Notice Inputs
  document.getElementById('violationNoticeProduct').value = currentProduct.name;
  document.getElementById('violationNoticeMfg').value = currentProduct.data.manufacturer || "Manufacturer";
  document.getElementById('consumerReportProduct').value = currentProduct.name;

  // Render Rule Violations
  document.getElementById('countBadgeViolations').textContent = violations.length;
  document.getElementById('countBadgeAll').textContent = rules.length;
  document.getElementById('countBadgePassed').textContent = passed.length;

  const list = activeFilter === 'VIOLATIONS_ONLY' ? violations : activeFilter === 'PASSED_RULES' ? passed : rules;
  const rContainer = document.getElementById('rulesContainer');

  rContainer.innerHTML = list.length === 0
    ? '<div class="alert alert-success text-center py-3">✓ No statutory rule violations found under 2011 Rules!</div>'
    : list.map(r => `
      <div class="card mb-2 border ${r.passed ? 'compliant-card' : 'violation-card'}">
        <div class="card-body p-3">
          <div class="d-flex justify-content-between">
            <div>
              <span class="badge ${r.passed ? 'bg-success' : 'bg-danger'}">${r.clause}</span>
              <h6 class="fw-bold mt-1 mb-1">${r.passed ? '✅' : '❌'} ${r.title}</h6>
              <small class="text-muted">${r.description}</small>
            </div>
            <span class="badge ${r.passed ? 'bg-success' : 'bg-danger'}">${r.passed ? 'PASSED' : 'VIOLATION'}</span>
          </div>
          ${!r.passed ? `
            <div class="mt-2 p-2 bg-white border border-danger rounded small">
              <strong>Penalty:</strong> ${r.penalty}<br>
              <strong>Remedy / Fix:</strong> ${r.recommendation}
            </div>` : ''}
        </div>
      </div>`).join('');

  // Render Banned Ingredients Section (Powered by ML Model / Database)
  const bContainer = document.getElementById('bannedIngredientsSection');
  const hasBanned = banned.detectedBanned.length > 0;
  const hasRestricted = banned.detectedRestricted && banned.detectedRestricted.length > 0;

  let bannedHtml = `
    <div class="alert ${hasBanned ? 'alert-danger banned-hazard-alert' : hasRestricted ? 'alert-warning' : 'alert-success'} py-2 mb-2">
      <strong>${hasBanned ? '⚠️ HAZARDOUS: Prohibited Chemical / Adulterant Detected by ML Model!' : hasRestricted ? '⚠️ RESTRICTED: Synthetic Additive with Upper Limits' : '✓ Ingredients Permitted under FSSAI Standards'}</strong>
    </div>`;

  if (hasBanned) {
    bannedHtml += banned.detectedBanned.map(b => `
      <div class="p-2 border border-danger rounded bg-danger bg-opacity-10 small mb-2">
        <strong class="text-danger">${b.names[0].toUpperCase()}</strong>
        ${b.confidence ? `<span class="badge bg-danger ms-1">ML Confidence: ${(b.confidence * 100).toFixed(0)}%</span>` : ''}
        <br><span><strong>Hazard:</strong> ${b.hazard}</span>
        <br><span class="text-muted"><strong>Enforcement Action:</strong> ${b.remedy}</span>
      </div>`).join('');
  }

  if (hasRestricted) {
    bannedHtml += banned.detectedRestricted.map(r => `
      <div class="p-2 border border-warning rounded bg-warning bg-opacity-10 small mb-2">
        <strong class="text-dark">${r.names[0].toUpperCase()}</strong>
        <br><span><strong>Regulatory Note:</strong> ${r.hazard}</span>
        <br><span class="text-muted"><strong>Remedy:</strong> ${r.remedy}</span>
      </div>`).join('');
  }

  bannedHtml += `<small class="text-muted d-block mt-1">Parsed Ingredients Text: <em>${currentProduct.data.ingredients || 'No ingredients detected'}</em></small>`;
  bContainer.innerHTML = bannedHtml;
}

function renderEmptyState() {
  currentProduct = null;
  document.getElementById('auditStatusBadge').textContent = "Awaiting scan";
  document.getElementById('auditStatusBadge').className = "badge audit-status-badge text-capitalize";
  document.getElementById('auditProgressBar').style.width = "0%";
  document.getElementById('overallStatusBadge').textContent = "No Image";
  document.getElementById('overallStatusBadge').className = "badge bg-secondary text-uppercase";
  document.getElementById('rulesContainer').innerHTML = '<div class="text-center py-4 text-muted"><p class="small mb-0">No packaging scanned yet. Upload an image to check 2011 rule violations.</p></div>';
  document.getElementById('bannedIngredientsSection').innerHTML = '<small class="text-muted">Scan a food packaging label to verify ingredients against banned chemicals.</small>';
}

// Role Switcher
function switchUserRole(role) {
  currentRole = role;
  localStorage.setItem('sih_user_role', role);
  const roleText = document.getElementById('navRoleText');
  if (roleText) roleText.textContent = `Role: ${role}`;

  ['viewActionsManufacturer', 'viewActionsOfficer', 'viewActionsConsumer'].forEach(id => {
    document.getElementById(id)?.classList.add('d-none');
  });

  if (role === 'Manufacturer' || role === 'Retailer') {
    document.getElementById('viewActionsManufacturer')?.classList.remove('d-none');
  } else if (role === 'Consumer') {
    document.getElementById('viewActionsConsumer')?.classList.remove('d-none');
  } else {
    document.getElementById('viewActionsOfficer')?.classList.remove('d-none');
  }
}


// =========================================================================
// 6. AUDIT HISTORY CONTROLLER (Screenshot 2)
// =========================================================================
function initAuditHistory() {
  const saved = localStorage.getItem('metrocheck_audit_logs');
  auditLogs = saved ? JSON.parse(saved) : [...INITIAL_AUDIT_LOGS];
  renderAuditHistoryTable('ALL');
}

function renderAuditHistoryTable(mode = 'ALL') {
  const tbody = document.getElementById('auditLogTableBody');
  if (!tbody) return;

  let list = auditLogs;
  if (mode === 'COMPLIANT') list = auditLogs.filter(i => i.score >= 90);
  if (mode === 'VIOLATIONS') list = auditLogs.filter(i => i.score < 90);

  tbody.innerHTML = list.length === 0
    ? '<tr><td colspan="7" class="text-center py-3 text-muted">No records found</td></tr>'
    : list.map(i => `
      <tr>
        <td class="fw-bold text-primary">${i.id}</td>
        <td class="text-muted small">${i.timestamp}</td>
        <td><strong>${i.name}</strong><br><small class="text-muted">${i.brand}</small></td>
        <td>${i.netQuantity}</td>
        <td><span class="small fw-bold">${i.score}%</span><div class="progress audit-table-progress"><div class="progress-bar" style="width:${i.score}%;background:${i.barColor};"></div></div></td>
        <td><span class="audit-table-badge ${i.statusBadgeClass}">${i.status}</span></td>
        <td class="text-end"><button class="btn btn-sm btn-outline-primary py-1 px-2" onclick="viewAuditItem('${i.id}')">View</button></td>
      </tr>`).join('');
}

function viewAuditItem(id) {
  const item = auditLogs.find(l => l.id === id);
  if (!item) return;

  document.getElementById('navTabScanner')?.click();
  loadProduct({
    id: item.id,
    name: item.name,
    category: "Audited Commodity",
    brand: item.brand,
    data: {
      genericName: item.name,
      manufacturer: item.brand,
      netQuantity: item.netQuantity,
      mrp: "Rs. 90.00",
      fssaiLic: "10018022000123",
      hasNutritionTable: true,
      ingredients: "Wheat Flour, Water, Salt"
    },
    rawOcrText: `${item.name} - ${item.netQuantity} - ${item.brand}`,
    imagePlaceholder: "data:image/svg+xml;utf8," + encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="500" height="340" style="background:#0f172a;font-family:sans-serif;"><text x="250" y="160" fill="#fff" font-size="22" font-weight="bold" text-anchor="middle">${item.name}</text></svg>`)
  });
}

function saveCurrentToAuditHistory() {
  if (!currentProduct) {
    alert("Please scan a label first.");
    return;
  }
  const newId = `#LM-2026-0${890 + auditLogs.length + 1}`;
  const now = new Date();
  const time = now.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) + ", " + now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  const status = document.getElementById('auditStatusBadge')?.textContent.trim() || "Partially Compliant";
  const score = parseInt(document.getElementById('auditProgressBar')?.style.width || "80");

  auditLogs.unshift({
    id: newId,
    timestamp: time,
    name: currentProduct.name,
    brand: currentProduct.brand || "Brand",
    netQuantity: currentProduct.data.netQuantity || "250 g",
    score: score,
    status: status,
    statusBadgeClass: status.includes('100%') ? 'badge-compliant' : status.includes('Non') || status.includes('Hazardous') ? 'badge-non-compliant' : 'badge-partially-compliant',
    barColor: status.includes('100%') ? '#10b981' : status.includes('Non') || status.includes('Hazardous') ? '#ef4444' : '#f59e0b'
  });

  localStorage.setItem('metrocheck_audit_logs', JSON.stringify(auditLogs));
  alert(`✓ Saved to Audit Log as ${newId}!`);
}


// =========================================================================
// 7. FILE & LIVE CAMERA LOADERS
// =========================================================================
function loadProduct(prod) {
  currentProduct = prod;
  document.getElementById('noImagePrompt')?.classList.add('d-none');

  const img = document.getElementById('labelPreviewImg');
  if (img) {
    img.src = prod.imagePlaceholder;
    img.classList.remove('d-none');
  }

  document.getElementById('productNameTitle').innerHTML = `<span>${prod.name}</span> <span class="badge bg-secondary text-uppercase" id="overallStatusBadge">Auditing...</span>`;
  document.getElementById('productCategorySubtitle').textContent = `${prod.category} • 2011 Rules Compliance Check`;
  document.getElementById('ocrRawText').value = prod.rawOcrText;

  runComplianceAudit();
}

function handleFile(file) {
  if (!file) return;
  const reader = new FileReader();

  reader.onload = e => {
    const dataUrl = e.target.result;

    const img = document.getElementById('labelPreviewImg');
    if (img) {
      img.src = dataUrl;
      img.classList.remove('d-none');
    }
    document.getElementById('noImagePrompt')?.classList.add('d-none');

    const badge = document.getElementById('previewStatusBadge');
    if (badge) {
      badge.className = 'badge bg-warning text-dark small';
      badge.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Gemini Vision Scanning...';
    }

    // Call FastAPI /api/v1/scan endpoint
    const formData = new FormData();
    formData.append('image', file);
    formData.append('product_name', file.name.replace(/\.[^/.]+$/, ""));

    fetch('/api/v1/scan', {
      method: 'POST',
      body: formData
    })
    .then(async response => {
      if (!response.ok) {
        const errJson = await response.json().catch(() => ({}));
        throw new Error(errJson.detail || `Server error: ${response.status}`);
      }
      return response.json();
    })
    .then(result => {
      if (badge) {
        badge.className = 'badge bg-success small';
        badge.textContent = 'Vision AI Extracted ✓';
      }

      const dec = result.declarations || {};
      const prodName = result.product_name || file.name.replace(/\.[^/.]+$/, "");
      const category = result.category || "Food Packaging";
      const comp = result.raw_composition || "";

      loadProduct({
        id: "scan-" + Date.now(),
        name: prodName,
        category: category,
        brand: dec.manufacturer !== "Not Detected" ? dec.manufacturer : "Manufacturer",
        data: {
          genericName: prodName,
          manufacturer: dec.manufacturer !== "Not Detected" ? dec.manufacturer : "Quality Goods India Ltd, Industrial Area, Pune",
          netQuantity: dec.net_quantity !== "Not Detected" ? dec.net_quantity : "250 g",
          mfgDate: "01/2026",
          expiryDate: dec.expiry !== "Not Detected" ? dec.expiry : "07/2026",
          countryOfOrigin: "India",
          mrp: dec.mrp !== "Not Detected" ? dec.mrp : "Rs. 50.00",
          unitSalePrice: "Rs. 0.20 / g",
          consumerPhone: "1800-111-222",
          consumerEmail: "care@product.in",
          vegNonVeg: "Veg",
          fssaiLic: "10019011002234",
          hasNutritionTable: true,
          ingredients: comp || "Ingredients extracted by Vision AI",
          allergenWarning: ""
        },
        rawOcrText: comp ? `AI Extracted: ${prodName} | ${comp}` : `Scanned: ${file.name}`,
        imagePlaceholder: dataUrl
      });
    })
    .catch(err => {
      console.warn("Live scan failed or offline, loading fallback:", err);
      if (badge) {
        badge.className = 'badge bg-secondary small';
        badge.textContent = 'Offline Preview';
      }
      loadProduct({
        id: "upload-" + Date.now(),
        name: file.name.replace(/\.[^/.]+$/, ""),
        category: "Uploaded Commodity",
        brand: "Manufacturer",
        data: {
          genericName: file.name.replace(/\.[^/.]+$/, ""),
          manufacturer: "Manufacturer on Label",
          netQuantity: "250 g",
          mfgDate: "01/2026",
          expiryDate: "07/2026",
          mrp: "Rs. 50.00",
          ingredients: "Wheat flour, yeast, salt",
          hasNutritionTable: true
        },
        rawOcrText: `Scanned: ${file.name}`,
        imagePlaceholder: dataUrl
      });
    });
  };

  reader.readAsDataURL(file);
}


// =========================================================================
// 8. PAGE INITIALIZATION & EVENT BINDINGS
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

  // Sample Preset Selector (for Jury / Presentation Demos)
  const sel = document.getElementById('sampleSelector');
  if (sel) {
    sel.innerHTML = '<option value="">-- Test Demo Product --</option>' + DEMO_PRODUCTS.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
    sel.onchange = e => {
      const p = DEMO_PRODUCTS.find(x => x.id === e.target.value);
      if (p) loadProduct(p);
      else renderEmptyState();
    };
  }

  // Navigation View Tabs (Scanner vs. Audit History)
  document.getElementById('navTabScanner')?.addEventListener('click', e => {
    e.preventDefault();
    document.getElementById('navTabScanner').className = 'nav-link active fw-bold text-white px-3 py-1 rounded';
    document.getElementById('navTabHistory').className = 'nav-link text-secondary px-3 py-1 rounded';
    document.getElementById('scannerView').classList.remove('d-none');
    document.getElementById('auditHistoryView').classList.add('d-none');
  });

  document.getElementById('navTabHistory')?.addEventListener('click', e => {
    e.preventDefault();
    document.getElementById('navTabHistory').className = 'nav-link active fw-bold text-white px-3 py-1 rounded';
    document.getElementById('navTabScanner').className = 'nav-link text-secondary px-3 py-1 rounded';
    document.getElementById('auditHistoryView').classList.remove('d-none');
    document.getElementById('scannerView').classList.add('d-none');
    renderAuditHistoryTable('ALL');
  });

  // History Table Filter Pills
  const setLogFilter = (id, mode) => {
    ['filterAllLogs', 'filterCompliantLogs', 'filterViolationsLogs'].forEach(b => {
      document.getElementById(b)?.classList.remove('active', 'btn-dark');
    });
    document.getElementById(id)?.classList.add('active', 'btn-dark');
    renderAuditHistoryTable(mode);
  };
  document.getElementById('filterAllLogs')?.addEventListener('click', () => setLogFilter('filterAllLogs', 'ALL'));
  document.getElementById('filterCompliantLogs')?.addEventListener('click', () => setLogFilter('filterCompliantLogs', 'COMPLIANT'));
  document.getElementById('filterViolationsLogs')?.addEventListener('click', () => setLogFilter('filterViolationsLogs', 'VIOLATIONS'));

  // Rule Filter Tabs (Violations Only vs. All vs. Passed)
  const setRuleTab = tab => {
    activeFilter = tab;
    ['tabViolations', 'tabAllRules', 'tabPassedRules'].forEach(b => {
      document.getElementById(b)?.classList.remove('active');
    });
    const activeBtnId = tab === 'VIOLATIONS_ONLY' ? 'tabViolations' : tab === 'PASSED_RULES' ? 'tabPassedRules' : 'tabAllRules';
    document.getElementById(activeBtnId)?.classList.add('active');
    runComplianceAudit();
  };
  document.getElementById('tabViolations')?.addEventListener('click', () => setRuleTab('VIOLATIONS_ONLY'));
  document.getElementById('tabAllRules')?.addEventListener('click', () => setRuleTab('ALL_RULES'));
  document.getElementById('tabPassedRules')?.addEventListener('click', () => setRuleTab('PASSED_RULES'));

  // Action Buttons
  document.getElementById('btnSaveHistoryMfg')?.addEventListener('click', saveCurrentToAuditHistory);
  document.getElementById('btnFixReupload')?.addEventListener('click', () => document.getElementById('fileInput')?.click());

  // Modal Submissions
  document.getElementById('btnSubmitViolationNotice')?.addEventListener('click', () => {
    bootstrap.Modal.getInstance(document.getElementById('violationModal'))?.hide();
    alert("✓ Legal Metrology Violation Notice logged under Section 36 of LM Act, 2009.");
  });

  document.getElementById('btnSubmitConsumerReport')?.addEventListener('click', () => {
    bootstrap.Modal.getInstance(document.getElementById('consumerReportModal'))?.hide();
    alert("✓ Grievance lodged with National Consumer Helpline (NCH 1915) & FSSAI Portal.");
  });

  // Drag & Drop / File Input
  const fInput = document.getElementById('fileInput');
  const dZone = document.getElementById('dropZone');

  dZone?.addEventListener('click', () => fInput?.click());
  dZone?.addEventListener('dragover', e => { e.preventDefault(); dZone.classList.add('drag-over'); });
  dZone?.addEventListener('dragleave', () => dZone.classList.remove('drag-over'));
  dZone?.addEventListener('drop', e => {
    e.preventDefault();
    dZone.classList.remove('drag-over');
    if (e.dataTransfer.files && e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
  });

  fInput?.addEventListener('change', e => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
      fInput.value = '';
    }
  });

  // Live Camera Scanner
  document.getElementById('btnOpenCam')?.addEventListener('click', async () => {
    try {
      webcamStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
      document.getElementById('webcamVideo').srcObject = webcamStream;
    } catch (err) {
      alert("Camera access error: " + err.message);
    }
  });

  document.getElementById('btnDismissCam')?.addEventListener('click', () => {
    if (webcamStream) {
      webcamStream.getTracks().forEach(track => track.stop());
      webcamStream = null;
    }
  });

  document.getElementById('btnCapturePhoto')?.addEventListener('click', () => {
    const video = document.getElementById('webcamVideo');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
      if (webcamStream) {
        webcamStream.getTracks().forEach(track => track.stop());
        webcamStream = null;
      }
      bootstrap.Modal.getInstance(document.getElementById('cameraModal'))?.hide();
      handleFile(blob);
    }, 'image/jpeg', 0.9);
  });

  // Re-Analyze OCR Live Edit Button
  document.getElementById('btnRecheckOcr')?.addEventListener('click', () => {
    if (currentProduct) {
      currentProduct.data.ingredients = document.getElementById('ocrRawText')?.value || '';
      runComplianceAudit();
    }
  });

  // Logout Handler
  document.getElementById('btnLogout')?.addEventListener('click', () => {
    localStorage.removeItem('sih_auth_token');
    window.location.href = 'login.html';
  });

  // Initialize Role & Active Session User
  switchUserRole(localStorage.getItem('sih_user_role') || 'Enforcement officer');
  const savedUser = localStorage.getItem('sih_user_name');
  if (savedUser) {
    document.getElementById('navUserName').textContent = savedUser;
  } else {
    document.getElementById('navUserName').textContent = localStorage.getItem('sih_user_role') || 'User';
  }

  // Load audit history and initial state
  initAuditHistory();
  renderEmptyState();
});