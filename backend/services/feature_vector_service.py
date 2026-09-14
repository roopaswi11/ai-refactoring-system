import csv
from pathlib import Path


class FeatureVectorService:

    @staticmethod
    def build_feature_vectors(metrics_file: str, sonar_issues: list):

        # ==========================================
        # 1. Read CK Metrics
        # ==========================================

        metrics_path = Path(metrics_file)

        if not metrics_path.is_absolute():
            metrics_path = Path(__file__).parent.parent / metrics_file

        metrics = []

        with open(metrics_path, "r", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                if not row.get("Class"):
                    continue

                metrics.append({
                    "Class": row["Class"],
                    "WMC": float(row.get("WMC", 0)),
                    "CBO": float(row.get("CBO", 0)),
                    "DIT": float(row.get("DIT", 0)),
                    "NOC": float(row.get("NOC", 0)),
                    "RFC": float(row.get("RFC", 0)),
                    "LCOM": float(row.get("LCOM", 0))
                })

        # ==========================================
        # 2. Organize SonarQube issues by file
        # ==========================================

        sonar_by_file = {}

        for issue in sonar_issues:

            file_name = Path(
                issue.get("file", "")
            ).name

            if not file_name:
                continue

            if file_name not in sonar_by_file:

                sonar_by_file[file_name] = {
                    "Code Smells": 0,
                    "Vulnerabilities": 0,
                    "Bugs": 0,
                    "Major Issues": 0,
                    "Minor Issues": 0,
                    "Blocker Issues": 0
                }

            issue_type = issue.get(
                "type", ""
            ).upper()

            severity = issue.get(
                "severity", ""
            ).upper()

            # Count issue type

            if issue_type == "CODE_SMELL":
                sonar_by_file[file_name]["Code Smells"] += 1

            elif issue_type == "VULNERABILITY":
                sonar_by_file[file_name]["Vulnerabilities"] += 1

            elif issue_type == "BUG":
                sonar_by_file[file_name]["Bugs"] += 1

            # Count severity

            if severity == "MAJOR":
                sonar_by_file[file_name]["Major Issues"] += 1

            elif severity == "MINOR":
                sonar_by_file[file_name]["Minor Issues"] += 1

            elif severity == "BLOCKER":
                sonar_by_file[file_name]["Blocker Issues"] += 1

        # ==========================================
        # 3. Combine CK Metrics + SonarQube
        # ==========================================

        feature_vectors = []

        for metric in metrics:

            class_name = metric["Class"]

            java_file = class_name + ".java"

            sonar_data = sonar_by_file.get(
                java_file,
                {
                    "Code Smells": 0,
                    "Vulnerabilities": 0,
                    "Bugs": 0,
                    "Major Issues": 0,
                    "Minor Issues": 0,
                    "Blocker Issues": 0
                }
            )

            vector = {

                "Class": class_name,

                # CK Metrics
                "WMC": metric["WMC"],
                "CBO": metric["CBO"],
                "DIT": metric["DIT"],
                "NOC": metric["NOC"],
                "RFC": metric["RFC"],
                "LCOM": metric["LCOM"],

                # SonarQube
                "Code Smells": sonar_data["Code Smells"],
                "Vulnerabilities": sonar_data["Vulnerabilities"],
                "Bugs": sonar_data["Bugs"],
                "Major Issues": sonar_data["Major Issues"],
                "Minor Issues": sonar_data["Minor Issues"],
                "Blocker Issues": sonar_data["Blocker Issues"]
            }

            feature_vectors.append(vector)

        # ==========================================
        # 4. Save the 12-feature vectors to CSV
        # ==========================================

        data_folder = Path(__file__).parent.parent / "data"

        data_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = data_folder / "feature_vectors.csv"

        fieldnames = [
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

        with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(feature_vectors)

        print("\n========== FEATURE VECTOR CSV ==========")
        print(f"Saved: {output_file}")
        print(f"Total classes: {len(feature_vectors)}")
        print("Total features per class: 12")
        print("========================================\n")

        return feature_vectors