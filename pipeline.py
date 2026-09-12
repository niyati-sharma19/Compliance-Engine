from typing import Dict, Any, List
from src.rules_engine import StatutoryRulesEngine
from src.explain import ComplianceExplainer

class EnterpriseComplianceEngine:
    def __init__(self):
        self.rules_engine = StatutoryRulesEngine()
        self.explainer = ComplianceExplainer()

    def inspect(self, category: str, product_name: str, composition: str) -> Dict[str, Any]:
        category = category.strip().upper()
        
        # Tier 1: Deterministic Statutory Enforcement
        passed_tier1, violations = self.rules_engine.evaluate(category, composition)
        
        if not passed_tier1:
            has_critical_ban = any(v.get("severity") == "STATUTORY_BAN" for v in violations)
            status = "PROHIBITED" if has_critical_ban else "HEALTH_HAZARD_WARNING"
            tier_name = "Tier 1: Statutory Authority Check" if has_critical_ban else "Tier 1: FSSAI / WHO Health Hazard Warning"
            risk = 1.0 if has_critical_ban else 0.85
            directive = (
                "Immediate product recall / formulation block."
                if has_critical_ban
                else "Health Advisory: Contains high-risk palm oil (saturated fat hazard). Reformulate with heart-healthy oils."
            )
            return {
                "product_name": product_name,
                "category": category,
                "overall_status": status,
                "tier_triggered": tier_name,
                "risk_score": risk,
                "regulatory_citations": violations,
                "action_required": directive
            }

        # Tier 2: Supervised ML Tree + Explainable AI (XAI)
        ml_analysis = self.explainer.explain_instance(category, composition)
        status = "FLAGGED_BY_MODEL" if ml_analysis["predicted_class"] == "PROHIBITED" else "COMPLIANT"

        return {
            "product_name": product_name,
            "category": category,
            "overall_status": status,
            "tier_triggered": "Tier 2: Supervised Tree Classifier",
            "risk_score": 1.0 - ml_analysis["confidence"] if status == "COMPLIANT" else ml_analysis["confidence"],
            "model_insights": {
                "salient_features": ml_analysis["salient_tokens"],
                "decision_path": ml_analysis["decision_path"][:3]
            },
            "action_required": "Review formula" if status != "COMPLIANT" else "Product cleared for distribution."
        }

if __name__ == "__main__":
    engine = EnterpriseComplianceEngine()

    test_cases = [
        ("AGRICULTURE", "Eco-Grow EC", "Emulsifiable concentrate containing Endosulfan and solvents"),
        ("COSMETICS", "Glow Whitening Day Cream", "Aqua, Glycerin, Stearic Acid, Mercury, Niacinamide"),
        ("MEDICINE", "Pediatric Drops", "Nimesulide syrup formulation 50mg"),
        ("COSMETICS", "Barrier Repair Cream", "Aqua, Shea Butter, Dimethicone, Tocopherol"),
        ("AGRICULTURE", "Bio-Neem Spray", "Cold pressed neem seed oil and azadirachtin")
    ]

    for cat, prod, comp in test_cases:
        print("\n" + "="*70)
        res = engine.inspect(cat, prod, comp)
        print(f"Product: {res['product_name']} | Category: {res['category']}")
        print(f"Status:  {res['overall_status']} | Engine: {res['tier_triggered']}")
        
        if "regulatory_citations" in res:
            for cit in res["regulatory_citations"]:
                print(f" -> [{cit['regulator']}] Clause: {cit['violation_reason']}")
        elif "model_insights" in res:
            print(f" -> Salient Tokens: {res['model_insights']['salient_features']}")
            print(f" -> Action: {res['action_required']}")