import pandas as pd
from scipy.io import arff
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

print("Loading phishing dataset...")

# =========================
# LOAD DATASET
# =========================

data, meta = arff.loadarff("phishing.arff")
df = pd.DataFrame(data)

# Convert byte columns to string
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].str.decode("utf-8")

# =========================
# SELECT ONLY URL-BASED FEATURES
# =========================

selected_features = [
    "having_IP_Address",
    "URL_Length",
    "Shortining_Service",
    "having_At_Symbol",
    "double_slash_redirecting",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "HTTPS_token"
]

X = df[selected_features]
y = df["Result"]

# Convert labels: -1 → 0 (Legitimate), 1 → 1 (Phishing)
y = y.apply(lambda x: 1 if str(x) == "1" else 0)

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# =========================
# OPTIMIZED SVM
# =========================

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(kernel="rbf"))
])

param_grid = {
    "svm__C": [0.1, 1, 10, 100],
    "svm__gamma": [0.01, 0.1, 1]
}

grid = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring="f1"
)

print("Training Optimized SVM...")
grid.fit(X_train, y_train)

print("Best Parameters:", grid.best_params_)

y_pred = grid.predict(X_test)
print(classification_report(y_test, y_pred))

# =========================
# SAVE MODEL
# =========================

joblib.dump(grid.best_estimator_, "optimized_model.pkl")

print("Final Optimized Model Saved Successfully!")
