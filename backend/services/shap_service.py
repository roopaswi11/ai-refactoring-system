import joblib
import pandas as pd
import shap

from pathlib import Path


class SHAPService:

    @staticmethod
    def explain(feature_vectors):

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
                f"Model not found: {model_path}"
            )

        model = joblib.load(model_path)

        # ==========================================
        # 2. Define 12 features
        # ==========================================

        features = [
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

        # ==========================================
        # 3. Convert input to DataFrame
        # ==========================================

        df = pd.DataFrame(feature_vectors)

        if df.empty:
            return []

        X = df[features].copy()

        # Make sure all features are numeric
        for feature in features:
            X[feature] = pd.to_numeric(
                X[feature],
                errors="coerce"
            ).fillna(0)

        # ==========================================
        # 4. Create SHAP explainer
        # ==========================================

        explainer = shap.TreeExplainer(model)

        shap_values = explainer.shap_values(X)

        print("\n========== SHAP DEBUG ==========")
        print(
            "SHAP type:",
            type(shap_values)
        )

        if isinstance(shap_values, list):

            print(
                "SHAP format: list"
            )

            print(
                "Number of outputs:",
                len(shap_values)
            )

            for i, value in enumerate(
                shap_values
            ):

                print(
                    f"Output {i} shape:",
                    value.shape
                )

        else:

            print(
                "SHAP shape:",
                shap_values.shape
            )

        print(
            "Model classes:",
            model.classes_
        )

        print(
            "================================\n"
        )

        # ==========================================
        # 5. Generate predictions
        # ==========================================

        predictions = model.predict(X)

        # ==========================================
        # 6. Generate explanations
        # ==========================================

        explanations = []

        for index in range(len(df)):

            class_name = str(
                df.iloc[index]["Class"]
            )

            prediction = predictions[index]

            # Find the output/class index
            class_index = list(
                model.classes_
            ).index(prediction)

            # ======================================
            # Handle SHAP output formats
            # ======================================

            if isinstance(shap_values, list):

                # Older SHAP versions
                values = shap_values[
                    class_index
                ][index]

            else:

                # Newer SHAP versions
                #
                # Possible shape:
                #
                # (samples, features, classes)
                #
                # or:
                #
                # (samples, features)

                if len(shap_values.shape) == 3:

                    values = shap_values[
                        index,
                        :,
                        class_index
                    ]

                elif len(shap_values.shape) == 2:

                    values = shap_values[
                        index,
                        :
                    ]

                else:

                    raise ValueError(
                        "Unexpected SHAP shape: "
                        f"{shap_values.shape}"
                    )

            # ======================================
            # Create explanation
            # ======================================

            explanation = {

                "Class": class_name,

                "Predicted Priority": str(
                    prediction
                ),

                "Contributions": []

            }

            # ======================================
            # Add feature contributions
            # ======================================

            for feature_index, feature in enumerate(
                features
            ):

                shap_value = values[
                    feature_index
                ]

                feature_value = X.iloc[
                    index
                ][feature]

                explanation[
                    "Contributions"
                ].append({

                    "Feature": feature,

                    "SHAP Value": float(
                        shap_value
                    ),

                    "Feature Value": float(
                        feature_value
                    )

                })

            # ======================================
            # Sort by strongest contribution
            # ======================================

            explanation[
                "Contributions"
            ].sort(

                key=lambda item:
                    abs(item["SHAP Value"]),

                reverse=True

            )

            explanations.append(
                explanation
            )

        return explanations