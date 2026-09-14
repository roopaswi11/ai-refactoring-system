import pandas as pd
from pathlib import Path


# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).parent

input_file = BASE_DIR / "data" / "feature_vectors.csv"
output_file = BASE_DIR / "data" / "training_data.csv"


# ==========================================
# 1. LOAD FUSED FEATURE DATA
# ==========================================

if not input_file.exists():
    raise FileNotFoundError(
        f"Feature vector file not found:\n{input_file}"
    )

df = pd.read_csv(input_file)

print("\n========== INPUT DATA ==========")
print(df)

print("\n========== COLUMNS ==========")
print(df.columns.tolist())


# ==========================================
# 2. CHECK REQUIRED FEATURES
# ==========================================

required_features = [
    "Class",
    "WMC",
    "CBO",
    "DIT",
    "NOC",
    "RFC",
    "LCOM",
    "Code Smells",
    "Vulnerabilities",
    "Bugs",
    "Major Issues",
    "Minor Issues",
    "Blocker Issues"
]

missing_columns = [
    column
    for column in required_features
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns in feature_vectors.csv: "
        f"{missing_columns}"
    )


# ==========================================
# 3. CONVERT NUMERIC FEATURES
# ==========================================

numeric_features = [
    "WMC",
    "CBO",
    "DIT",
    "NOC",
    "RFC",
    "LCOM",
    "Code Smells",
    "Vulnerabilities",
    "Bugs",
    "Major Issues",
    "Minor Issues",
    "Blocker Issues"
]

for column in numeric_features:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    df[column] = df[column].fillna(0)


# ==========================================
# 4. CALCULATE REFACTORING RISK SCORE
# ==========================================

def calculate_priority_score(row):

    score = 0

    # --------------------------------------
    # CK Metrics
    # --------------------------------------

    # WMC - Weighted Methods per Class
    if row["WMC"] > 20:
        score += 2

    elif row["WMC"] > 10:
        score += 1


    # CBO - Coupling Between Objects
    if row["CBO"] > 10:
        score += 2

    elif row["CBO"] > 5:
        score += 1


    # RFC - Response For a Class
    if row["RFC"] > 100:
        score += 2

    elif row["RFC"] > 50:
        score += 1


    # LCOM - Lack of Cohesion
    if row["LCOM"] > 5:
        score += 2

    elif row["LCOM"] > 2:
        score += 1


    # --------------------------------------
    # SonarQube Metrics
    # --------------------------------------

    # Vulnerabilities
    score += int(row["Vulnerabilities"]) * 3


    # Bugs
    score += int(row["Bugs"]) * 2


    # Blocker Issues
    score += int(row["Blocker Issues"]) * 4


    # Major Issues
    score += int(row["Major Issues"]) * 2


    # Code Smells
    if row["Code Smells"] >= 10:
        score += 2

    elif row["Code Smells"] >= 5:
        score += 1


    return score


# ==========================================
# 5. GENERATE SCORE
# ==========================================

df["priority_score"] = df.apply(
    calculate_priority_score,
    axis=1
)


print("\n========== PRIORITY SCORES ==========")

print(
    df[
        [
            "Class",
            "priority_score"
        ]
    ]
)


# ==========================================
# 6. CREATE LOW / MEDIUM / HIGH LABELS
# ==========================================

# We rank the classes by their priority score.
#
# qcut divides the ranked classes into three
# approximately equal groups.


df["refactoring_priority"] = pd.qcut(
    df["priority_score"].rank(
        method="first"
    ),
    q=3,
    labels=[
        "LOW",
        "MEDIUM",
        "HIGH"
    ]
)


# ==========================================
# 7. REMOVE INTERNAL SCORE
# ==========================================

df = df.drop(
    columns=[
        "priority_score"
    ]
)


# ==========================================
# 8. DISPLAY GENERATED LABELS
# ==========================================

print("\n========== GENERATED PRIORITIES ==========")

print(
    df[
        [
            "Class",
            "refactoring_priority"
        ]
    ]
)


# ==========================================
# 9. DISPLAY DISTRIBUTION
# ==========================================

print("\n========== PRIORITY DISTRIBUTION ==========")

print(
    df[
        "refactoring_priority"
    ].value_counts()
)


# ==========================================
# 10. SAVE TRAINING DATA
# ==========================================

output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    output_file,
    index=False
)


# ==========================================
# 11. FINAL OUTPUT
# ==========================================

print("\n==========================================")
print("Training dataset created successfully!")
print(f"Location: {output_file}")
print(f"Total classes: {len(df)}")
print("Features: 12")
print("Target: refactoring_priority")
print("==========================================")