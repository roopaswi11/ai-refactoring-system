import pandas as pd
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# 1. PATHS
# ==========================================

BASE_DIR = Path(__file__).parent

data_file = (
    BASE_DIR
    / "data"
    / "training_data.csv"
)

model_file = (
    BASE_DIR
    / "models"
    / "refactoring_model.pkl"
)


# ==========================================
# 2. LOAD DATA
# ==========================================

if not data_file.exists():

    raise FileNotFoundError(
        f"Training data not found:\n{data_file}"
    )


df = pd.read_csv(data_file)


print("\n========== TRAINING DATA ==========")

print(df)

print("\nColumns:")

print(
    df.columns.tolist()
)


# ==========================================
# 3. DEFINE 12 FEATURES
# ==========================================

features = [

    # CK Metrics
    "WMC",
    "CBO",
    "DIT",
    "NOC",
    "RFC",
    "LCOM",

    # SonarQube Metrics
    "Code Smells",
    "Vulnerabilities",
    "Bugs",
    "Major Issues",
    "Minor Issues",
    "Blocker Issues"
]


target = "refactoring_priority"


# ==========================================
# 4. CHECK FEATURES
# ==========================================

missing_features = [

    feature

    for feature in features

    if feature not in df.columns
]


if missing_features:

    raise ValueError(
        f"Missing features: {missing_features}"
    )


if target not in df.columns:

    raise ValueError(
        "refactoring_priority column missing!"
    )


# ==========================================
# 5. CREATE X AND Y
# ==========================================

X = df[features]

y = df[target]


print("\n========== INPUT FEATURES ==========")

print(
    f"Number of features: {len(features)}"
)

print(
    features
)


print("\n========== TARGET DISTRIBUTION ==========")

print(
    y.value_counts()
)


# ==========================================
# 6. TRAIN RANDOM FOREST
# ==========================================

model = RandomForestClassifier(

    n_estimators=200,

    random_state=42,

    class_weight="balanced",

    max_depth=8

)


model.fit(
    X,
    y
)


# ==========================================
# 7. TRAINING PREDICTIONS
# ==========================================

predictions = model.predict(X)


accuracy = accuracy_score(
    y,
    predictions
)


print("\n========== MODEL RESULT ==========")

print(
    f"Training Accuracy: {accuracy:.2f}"
)


print("\nClassification Report:")

print(
    classification_report(
        y,
        predictions,
        zero_division=0
    )
)


# ==========================================
# 8. FEATURE IMPORTANCE
# ==========================================

importance = pd.DataFrame({

    "Feature": features,

    "Importance":
        model.feature_importances_

})


importance = importance.sort_values(

    by="Importance",

    ascending=False

)


print("\n========== FEATURE IMPORTANCE ==========")

print(
    importance.to_string(
        index=False
    )
)


# ==========================================
# 9. SAVE MODEL
# ==========================================

model_file.parent.mkdir(

    parents=True,

    exist_ok=True

)


joblib.dump(

    model,

    model_file

)


print("\n===================================")

print(
    "Random Forest model saved!"
)

print(
    f"Location: {model_file}"
)

print(
    "Features used: 12"
)

print(
    "Target: refactoring_priority"
)

print("===================================")