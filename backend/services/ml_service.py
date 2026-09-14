import joblib
import pandas as pd
from pathlib import Path


class MLService:

    @staticmethod
    def predict(feature_vectors):

        # ==========================================
        # 1. Load trained Random Forest
        # ==========================================

        model_path = (
            Path(__file__).parent.parent
            / "models"
            / "refactoring_model.pkl"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Random Forest model not found: {model_path}"
            )

        model = joblib.load(model_path)

        # ==========================================
        # 2. Define the 12 features
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

        # ==========================================
        # 3. Convert feature vectors to DataFrame
        # ==========================================

        df = pd.DataFrame(
            feature_vectors
        )

        if df.empty:
            return []

        # ==========================================
        # 4. Check all features exist
        # ==========================================

        missing_features = [
            feature
            for feature in features
            if feature not in df.columns
        ]

        if missing_features:

            raise ValueError(
                "Missing features: "
                f"{missing_features}"
            )

        # ==========================================
        # 5. Prepare ML input
        # ==========================================

        X = df[features].copy()

        for feature in features:

            X[feature] = pd.to_numeric(
                X[feature],
                errors="coerce"
            ).fillna(0)

        # ==========================================
        # 6. Random Forest prediction
        # ==========================================

        predictions = model.predict(X)

        # ==========================================
        # 7. Random Forest probabilities
        # ==========================================

        probabilities = model.predict_proba(X)

        classes = model.classes_

        # ==========================================
        # 8. Build results
        # ==========================================

        results = []

        for i, prediction in enumerate(
            predictions
        ):

            # Convert probability array
            # into a readable dictionary

            probability_dict = {

                str(classes[j]):
                float(probabilities[i][j])

                for j in range(
                    len(classes)
                )
            }

            result = {

                "Class": str(
                    df.iloc[i]["Class"]
                ),

                # ------------------------------
                # CK Metrics
                # ------------------------------

                "WMC": float(
                    df.iloc[i]["WMC"]
                ),

                "CBO": float(
                    df.iloc[i]["CBO"]
                ),

                "DIT": float(
                    df.iloc[i]["DIT"]
                ),

                "NOC": float(
                    df.iloc[i]["NOC"]
                ),

                "RFC": float(
                    df.iloc[i]["RFC"]
                ),

                "LCOM": float(
                    df.iloc[i]["LCOM"]
                ),

                # ------------------------------
                # SonarQube Metrics
                # ------------------------------

                "Code Smells": int(
                    df.iloc[i]["Code Smells"]
                ),

                "Vulnerabilities": int(
                    df.iloc[i]["Vulnerabilities"]
                ),

                "Bugs": int(
                    df.iloc[i]["Bugs"]
                ),

                "Major Issues": int(
                    df.iloc[i]["Major Issues"]
                ),

                "Minor Issues": int(
                    df.iloc[i]["Minor Issues"]
                ),

                "Blocker Issues": int(
                    df.iloc[i]["Blocker Issues"]
                ),

                # ------------------------------
                # Prediction
                # ------------------------------

                "refactoring_priority": str(
                    prediction
                ),

                # ------------------------------
                # Prediction Probabilities
                # ------------------------------

                "prediction_probabilities":
                    probability_dict
            }

            results.append(
                result
            )

        return results