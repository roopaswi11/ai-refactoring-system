import pandas as pd

from services.shap_service import SHAPService


# ==========================================
# Load feature vectors
# ==========================================

df = pd.read_csv(
    "data/feature_vectors.csv"
)

feature_vectors = df.to_dict(
    orient="records"
)


# ==========================================
# Generate SHAP explanations
# ==========================================

results = SHAPService.explain(
    feature_vectors
)


# ==========================================
# Display results
# ==========================================

print("\n======================================")
print("SHAP EXPLANATIONS")
print("======================================")

for result in results:

    print(
        f"\nClass: {result['Class']}"
    )

    print(
        f"Predicted Priority: "
        f"{result['Predicted Priority']}"
    )

    print("\nTop contributing features:")

    for contribution in result[
        "Contributions"
    ][:5]:

        print(
            f"  {contribution['Feature']}: "
            f"{contribution['SHAP Value']:.4f} "
            f"(value={contribution['Feature Value']})"
        )