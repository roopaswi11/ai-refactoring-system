from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

from services.zip_service import extract_zip
from services.metrics_service import MetricsService
from services.sonarqube_service import SonarQubeService
from services.sonar_results_service import SonarResultsService
from services.feature_vector_service import FeatureVectorService
from services.ml_service import MLService
from services.shap_service import SHAPService
from services.impact_service import ImpactService


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


UPLOAD_FOLDER = Path("uploads")
EXTRACT_FOLDER = Path("extracted_projects")

UPLOAD_FOLDER.mkdir(
    exist_ok=True
)

EXTRACT_FOLDER.mkdir(
    exist_ok=True
)


@router.post("/")
async def upload_project(
    file: UploadFile = File(...)
):

    # ==========================================
    # 1. Check ZIP file
    # ==========================================

    if not file.filename.lower().endswith(".zip"):

        return {
            "status": "error",
            "message": "Only ZIP files are allowed"
        }


    # ==========================================
    # 2. Save uploaded ZIP
    # ==========================================

    zip_path = (
        UPLOAD_FOLDER /
        file.filename
    )

    with open(
        zip_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    # ==========================================
    # 3. Extract project
    # ==========================================

    project_folder = (
        EXTRACT_FOLDER /
        file.filename.replace(
            ".zip",
            ""
        )
    )

    extract_zip(
        zip_path,
        project_folder
    )

    print(
        "Project extracted:",
        project_folder
    )


    # ==========================================
    # 4. Run CK Metrics
    # ==========================================

    MetricsService.run_metrics(
        str(project_folder)
    )

    metrics_path = Path(
        "metrics.csv"
    )

    print(
        "CK Metrics completed."
    )


    # ==========================================
    # 5. Run SonarQube
    # ==========================================

    SonarQubeService.run_analysis(
        str(project_folder)
    )

    print(
        "SonarQube analysis completed."
    )


    # ==========================================
    # 6. Get SonarQube issues
    # ==========================================

    sonar_results = SonarResultsService.get_results(
        str(project_folder)
    )

    print(
        "SonarQube issues:"
    )

    print(
        sonar_results
    )


    # ==========================================
    # 7. Build 12-feature vectors
    # ==========================================

    feature_vectors = (
        FeatureVectorService
        .build_feature_vectors(
            "metrics.csv",
            sonar_results
        )
    )

    print(
        "\n========== FEATURE VECTORS =========="
    )

    for vector in feature_vectors:

        print(vector)


    # ==========================================
    # 8. Random Forest prediction
    # ==========================================

    predictions = (
        MLService.predict(
            feature_vectors
        )
    )

    print(
        "\n========== RANDOM FOREST PREDICTIONS =========="
    )

    print(
        predictions
    )


    # ==========================================
    # 9. SHAP explanations
    # ==========================================

    shap_results = (
        SHAPService.explain(
            feature_vectors
        )
    )

    # ==========================================
    # 10. Calculate Refactoring Impact
    # ==========================================

    impact_results = ImpactService.calculate_impact(
        feature_vectors
    )

    print(
        "\n========== REFACTORING IMPACT =========="
    )

    for result in impact_results:

        print(
            f"\nClass: {result['Class']}"
        )

        print(
            f"Impact Score: "
            f"{result['impact_score']}"
        )

        print(
            f"Impact Level: "
            f"{result['impact_level']}"
        )

        print(
            "Expected Benefits:"
        )

        for benefit in result[
            "expected_benefits"
        ]:

            print(
                f"  - {benefit}"
            )

    print(
        "\n========== SHAP EXPLANATIONS =========="
    )

    for result in shap_results:

        print(
            f"\nClass: "
            f"{result['Class']}"
        )

        print(
            f"Priority: "
            f"{result['Predicted Priority']}"
        )

        print(
            "Top contributing features:"
        )

        for contribution in (
            result["Contributions"][:5]
        ):

            print(
                f"  "
                f"{contribution['Feature']} "
                f"→ "
                f"{contribution['SHAP Value']:.4f}"
            )

    # ==========================================
    # 10. Return final response
    # ==========================================
    return {
        "status": "success",
        "project": file.filename,
        "location": str(project_folder),

        "feature_vectors": feature_vectors,

        "predictions": predictions,

        "shap_explanations": shap_results,

        "impact_results": impact_results
    }