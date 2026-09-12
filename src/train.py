from pathlib import Path
from typing import Optional
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "standardized_products.csv"
DEFAULT_MODELS_DIR = PROJECT_ROOT / "models"

def train_compliance_model(data_path: Optional[str] = None):
    target_data_path = Path(data_path) if data_path else DEFAULT_DATA_PATH
    df = pd.read_csv(target_data_path)
    
    # Train strictly on ingredient/formulation tokens
    X = df["clean_composition"].fillna("")
    y = df["is_banned"]

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=300,
            token_pattern=r"(?u)\b[a-zA-Z0-9_-]{2,}\b"
        )),
        ("clf", DecisionTreeClassifier(
            max_depth=5,
            min_samples_split=3,
            min_samples_leaf=2,
            random_state=42
        ))
    ])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(pipeline, X, y, cv=cv, scoring="accuracy")
    print(f"\n--- 5-Fold Stratified Cross-Validation Accuracy ---")
    print(f"Mean Accuracy: {scores.mean():.2f} (Std: {scores.std():.2f})")

    # Fit on full dataset
    pipeline.fit(X, y)

    y_pred = pipeline.predict(X)
    print("\n--- Training Set Evaluation Report ---")
    print(classification_report(y, y_pred, target_names=["Compliant", "Prohibited"], zero_division=0))

    # Save pipeline
    DEFAULT_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    pipeline_file = DEFAULT_MODELS_DIR / "compliance_tree_pipeline.pkl"
    joblib.dump(pipeline, pipeline_file)
    print(f"Saved pipeline to {pipeline_file}")

    # Export inspectable decision rules
    feature_names = pipeline.named_steps["tfidf"].get_feature_names_out()
    tree_rules = export_text(pipeline.named_steps["clf"], feature_names=list(feature_names))
    rules_file = DEFAULT_MODELS_DIR / "decision_tree_rules.txt"
    with open(rules_file, "w", encoding="utf-8") as f:
        f.write(tree_rules)
    print(f"Exported updated decision logic to {rules_file}")

if __name__ == "__main__":
    train_compliance_model()