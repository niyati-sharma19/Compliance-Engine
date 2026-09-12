from pathlib import Path
from typing import Optional
import joblib
import numpy as np
from src.preprocessor import ProductDatasetPreprocessor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "compliance_tree_pipeline.pkl"

class ComplianceExplainer:
    def __init__(self, model_path: Optional[str] = None):
        target_path = Path(model_path) if model_path else DEFAULT_MODEL_PATH
        self.pipeline = joblib.load(target_path)
        self.vectorizer = self.pipeline.named_steps["tfidf"]
        self.tree = self.pipeline.named_steps["clf"]
        self.feature_names = np.array(self.vectorizer.get_feature_names_out())
        self.preprocessor = ProductDatasetPreprocessor()

    def explain_instance(self, category: str, composition: str) -> dict:
        # Normalize text cleanly matching the training pipeline
        text = self.preprocessor.normalize_text(composition)
        
        vec = self.vectorizer.transform([text])
        probabilities = self.pipeline.predict_proba([text])[0]
        prob_prohibited = probabilities[1]

        # Extract tokens that actively fired
        active_indices = vec.indices
        active_tokens = self.feature_names[active_indices] if len(active_indices) > 0 else np.array([])
        
        token_weights = []
        if len(active_indices) > 0:
            token_weights = sorted(
                zip(active_tokens, vec.data),
                key=lambda x: x[1],
                reverse=True
            )

        # Tracing decision path
        node_indicator = self.tree.decision_path(vec)
        feature_indices = self.tree.tree_.feature

        decision_steps = []
        for node_id in node_indicator.indices:
            feat_idx = feature_indices[node_id]
            if feat_idx != -2:
                feat_name = self.feature_names[feat_idx]
                val = vec[0, feat_idx]
                thresh = self.tree.tree_.threshold[node_id]
                decision_steps.append(f"{feat_name} ({val:.2f}) {'<=' if val <= thresh else '>'} {thresh:.2f}")

        # Classification decision threshold at 0.50
        predicted_class = "PROHIBITED" if prob_prohibited >= 0.50 else "COMPLIANT"
        confidence = float(prob_prohibited if predicted_class == "PROHIBITED" else 1.0 - prob_prohibited)

        return {
            "predicted_class": predicted_class,
            "confidence": round(confidence, 3),
            "salient_tokens": [tok for tok, _ in token_weights[:5]],
            "decision_path": decision_steps
        }

if __name__ == "__main__":
    explainer = ComplianceExplainer()
    test_result = explainer.explain_instance("COSMETICS", "Aqua, Glycerin, Sodium Chloride")
    print("\nResult:", test_result)