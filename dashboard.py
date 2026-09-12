import os
import io
import streamlit as st
from PIL import Image

from pipeline import EnterpriseComplianceEngine
from src.report_generator import ComplianceAuditReporter

try:
    from src.ai_studio_vision import AIStudioVisionExtractor
    vision_extractor = AIStudioVisionExtractor()
    ai_vision_ready = True
except Exception as e:
    vision_extractor = None
    ai_vision_ready = False
    vision_init_error = str(e)

# Page configuration
st.set_page_config(
    page_title="Regulatory Compliance Engine",
    page_icon="🛡️",
    layout="wide"
)

# Initialize engine (cached so it loads only once)
@st.cache_resource
def load_engine():
    return EnterpriseComplianceEngine()

engine = load_engine()

# Header banner
st.title("🛡️ Multi-Sector Regulatory Compliance & Risk Audit")
st.markdown(
    "Automated statutory verification and explainable ML scoring for **Food (FSSAI)**, "
    "**Cosmetics (CDSCO/BIS)**, **Medicine (CDSCO)**, and **Agriculture (CIBRC)**."
)
st.divider()

# Sidebar: Benchmark Presets & Configuration
st.sidebar.header("⚙️ Configuration & Presets")
if ai_vision_ready:
    st.sidebar.success("✅ Google Gemini Vision: **ACTIVE**")
else:
    st.sidebar.warning(f"⚠️ Gemini Vision: Inactive ({vision_init_error})")

preset_options = {
    "Custom Formulation": {
        "category": "FOOD",
        "product_name": "",
        "composition": ""
    },
    "Lay's Potato Chips (Palm Oil / Palmolein)": {
        "category": "FOOD",
        "product_name": "Lay's Classic Potato Chips",
        "composition": "Potatoes, Edible Vegetable Oil (Palmolein), Iodised Salt"
    },
    "Banned Bakery Bread (FSSAI)": {
        "category": "FOOD",
        "product_name": "Premium White Loaf",
        "composition": "Refined wheat flour, water, yeast, potassium bromate, salt"
    },
    "Banned Skin Cream (CDSCO/BIS)": {
        "category": "COSMETICS",
        "product_name": "Ultra Glow Treatment",
        "composition": "Aqua, Glycerin, Stearic Acid, Mercury, Niacinamide"
    },
    "Restricted Pediatric Drug (CDSCO)": {
        "category": "MEDICINE",
        "product_name": "Fever Relief Suspension",
        "composition": "Nimesulide 50mg flavored syrup"
    },
    "Banned Agro-Pesticide (CIBRC)": {
        "category": "AGRICULTURE",
        "product_name": "Pest-Guard 35 EC",
        "composition": "Endosulfan 35% EC, aromatic solvent, emulsifiers"
    },
    "Safe Basmati Grain (Cleared)": {
        "category": "FOOD",
        "product_name": "Royal Brown Rice",
        "composition": "100% whole grain brown rice"
    },
    "Safe Cosmetic Cleanser (Cleared)": {
        "category": "COSMETICS",
        "product_name": "Hydra Gentle Cleanser",
        "composition": "Aqua, Glycerin, Sodium Chloride, Cocamidopropyl Betaine"
    }
}

selected_preset = st.sidebar.selectbox("Load a sample case:", list(preset_options.keys()))
preset_data = preset_options[selected_preset]

# Input Form & Output Layout
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    tab_image, tab_manual = st.tabs(["📷 Upload Label Image (AI Auto-Audit)", "✍️ Manual Form & Presets"])

    with tab_image:
        st.subheader("Step 1: Upload Product Packaging Photo")
        st.caption("Upload a front or back panel image. Google Gemini Vision will automatically extract the ingredients, product name, and Legal Metrology declarations.")

        image_source = st.radio("Choose Image Source:", ["📁 Upload File", "📸 Use Webcam"], horizontal=True)

        uploaded_image = None
        if image_source == "📁 Upload File":
            uploaded_file = st.file_uploader(
                "Choose packaging image",
                type=["jpg", "jpeg", "png", "webp"],
                help="Accepts high-resolution photos of packaging labels"
            )
            if uploaded_file:
                uploaded_image = Image.open(uploaded_file)
        else:
            camera_file = st.camera_input("Take a photo of the product packaging label")
            if camera_file:
                uploaded_image = Image.open(camera_file)

        if uploaded_image:
            st.image(uploaded_image, caption="Label Preview", use_container_width=True)

        scan_button = st.button("🚀 Analyze & Audit Label Image", type="primary", use_container_width=True, disabled=(uploaded_image is None))

    with tab_manual:
        st.subheader("Manual Formulation Details")
        manual_category = st.selectbox(
            "Product Domain / Category",
            options=["FOOD", "COSMETICS", "MEDICINE", "AGRICULTURE"],
            index=["FOOD", "COSMETICS", "MEDICINE", "AGRICULTURE"].index(preset_data["category"]),
            key="manual_category"
        )
        
        manual_product_name = st.text_input(
            "Product Trade Name",
            value=preset_data["product_name"],
            placeholder="e.g., Organic Multigrain Bread",
            key="manual_product_name"
        )
        
        manual_composition = st.text_area(
            "Ingredients / Chemical Composition",
            value=preset_data["composition"],
            placeholder="e.g., Wheat flour, water, yeast, potassium bromate, salt",
            height=140,
            key="manual_composition"
        )
        
        manual_inspect_btn = st.button("Run Compliance Audit on Manual Input", type="primary", use_container_width=True)

# Inspection Output
with col_output:
    st.subheader("Audit Results & Explanations")

    audit_result = None
    extracted_declarations = None
    product_display_name = ""
    category_display = ""

    # 1. Processing Image Scan
    if scan_button and uploaded_image:
        if not ai_vision_ready or vision_extractor is None:
            st.error("Google AI Studio Vision is not initialized. Ensure GEMINI_API_KEY is set in your environment.")
        else:
            with st.spinner("🤖 Google Gemini Vision is reading packaging text and declarations..."):
                try:
                    label_data = vision_extractor.extract_label_data(uploaded_image)
                    extracted_declarations = {
                        "Product Name": label_data.product_name,
                        "Inferred Sector": label_data.inferred_category,
                        "MRP": label_data.mrp,
                        "Net Quantity": label_data.net_quantity,
                        "Manufacturer": label_data.manufacturer_info,
                        "Expiry / Best Before": label_data.expiry_or_best_before,
                        "Ingredients": label_data.raw_composition_text or ", ".join(label_data.ingredients_list)
                    }

                    product_display_name = label_data.product_name
                    category_display = label_data.inferred_category

                    with st.spinner("Screening statutory databases and evaluating ML tree..."):
                        audit_result = engine.inspect(
                            category=label_data.inferred_category,
                            product_name=label_data.product_name,
                            composition=extracted_declarations["Ingredients"]
                        )
                except Exception as e:
                    st.error(f"Vision Extraction Error: {e}")

    # 2. Processing Manual Input
    elif manual_inspect_btn:
        if not manual_product_name.strip() or not manual_composition.strip():
            st.warning("Please provide both a Product Name and Ingredients/Composition.")
        else:
            product_display_name = manual_product_name
            category_display = manual_category
            with st.spinner("Screening statutory databases and evaluating ML tree..."):
                audit_result = engine.inspect(
                    category=manual_category,
                    product_name=manual_product_name,
                    composition=manual_composition
                )

    # Display Results if Available
    if audit_result:
        # Show Extracted Legal Metrology Declarations if from image
        if extracted_declarations:
            st.markdown("#### 📦 Extracted Legal Metrology Declarations")
            dec_col1, dec_col2 = st.columns(2)
            with dec_col1:
                st.info(f"**MRP:** {extracted_declarations['MRP']}\n\n**Net Qty:** {extracted_declarations['Net Quantity']}")
            with dec_col2:
                st.info(f"**Mfg/Packer:** {extracted_declarations['Manufacturer']}\n\n**Expiry:** {extracted_declarations['Expiry / Best Before']}")
            
            with st.expander("📋 Legible Ingredients Extracted by Vision AI", expanded=True):
                st.write(extracted_declarations["Ingredients"])

        # Display Status Banner
        status = audit_result["overall_status"]
        if status == "PROHIBITED":
            st.error(f"### Status: ⛔ PROHIBITED / NON-COMPLIANT")
        elif status == "HEALTH_HAZARD_WARNING":
            st.warning(f"### Status: ⚠️ HEALTH HAZARD / NUTRITIONAL WARNING")
        elif status == "COMPLIANT":
            st.success(f"### Status: ✅ COMPLIANT / CLEARED")
        else:
            st.warning(f"### Status: ⚠️ {status}")

        st.write(f"**Product:** `{audit_result['product_name']}` | **Category:** `{audit_result['category']}`")
        st.write(f"**Engine Triggered:** `{audit_result['tier_triggered']}`")
        st.write(f"**Risk Level:** `{audit_result['risk_score'] * 100:.1f}%`")
        st.write(f"**Directive:** {audit_result['action_required']}")

        st.divider()

        # Tier 1 Breakdown
        if "regulatory_citations" in audit_result and audit_result["regulatory_citations"]:
            st.markdown("#### 🚨 Statutory Prohibitions Detected")
            for cit in audit_result["regulatory_citations"]:
                with st.expander(f"Violation: {cit.get('flagged_ingredient')}", expanded=True):
                    st.markdown(f"**Authority:** `{cit.get('regulator')}`")
                    st.markdown(f"**Clause / Legal Reason:** {cit.get('violation_reason')}")

        # Tier 2 ML Explainability Breakdown
        elif "model_insights" in audit_result:
            st.markdown("#### 🧠 Explainable AI Decision Breakdown")
            insights = audit_result["model_insights"]
            
            st.markdown(f"**Salient Ingredient Tokens:** `{', '.join(insights['salient_features']) if insights['salient_features'] else 'None (Neutral Base)'}`")
            
            with st.expander("Decision Tree Logic Splits", expanded=True):
                for step in insights.get("decision_path", []):
                    st.code(step, language="text")

        # Formatted Downloadable Audit Report
        audit_report_str = ComplianceAuditReporter.generate_text_audit(audit_result)
        
        st.download_button(
            label="📄 Download Official Compliance Certificate (.txt)",
            data=audit_report_str,
            file_name=f"audit_{product_display_name.lower().replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    elif not scan_button and not manual_inspect_btn:
        st.info("👈 Upload an image or select a preset, then click **Analyze & Audit** to view results.")