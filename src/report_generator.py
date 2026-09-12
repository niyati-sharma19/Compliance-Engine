from datetime import datetime
from typing import Dict, Any

class ComplianceAuditReporter:
    @staticmethod
    def generate_text_audit(inspection_result: Dict[str, Any]) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
        status = inspection_result.get("overall_status", "UNKNOWN")
        prod_name = inspection_result.get("product_name", "N/A")
        category = inspection_result.get("category", "N/A")
        tier = inspection_result.get("tier_triggered", "N/A")
        
        divider = "=" * 65
        sub_divider = "-" * 65

        lines = [
            divider,
            f"          STATUTORY COMPLIANCE & RISK AUDIT REPORT",
            divider,
            f" Timestamp       : {timestamp}",
            f" Product Name    : {prod_name}",
            f" Sector / Domain : {category}",
            f" Clearance State : {status}",
            f" Engine Tier     : {tier}",
            sub_divider
        ]

        if "regulatory_citations" in inspection_result and inspection_result["regulatory_citations"]:
            lines.append(" REGULATORY INFRACTIONS (STATUTORY BLOCK):")
            for idx, cit in enumerate(inspection_result["regulatory_citations"], 1):
                lines.append(f"  [{idx}] Substance : {cit.get('flagged_ingredient')}")
                lines.append(f"      Authority : {cit.get('regulator')}")
                lines.append(f"      Violation : {cit.get('violation_reason')}")
        elif "model_insights" in inspection_result:
            insights = inspection_result["model_insights"]
            lines.append(" TIER-2 MACHINE LEARNING EVALUATION TRACE:")
            lines.append(f"  Risk Confidence  : {inspection_result.get('risk_score', 0.0)}")
            lines.append(f"  Active Tokens    : {', '.join(insights.get('salient_features', []))}")
            lines.append("  Decision Splits  :")
            for step in insights.get("decision_path", []):
                lines.append(f"    • {step}")

        lines.extend([
            sub_divider,
            f" Action Directive : {inspection_result.get('action_required', 'N/A')}",
            divider
        ])

        return "\n".join(lines)