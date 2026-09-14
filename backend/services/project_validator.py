from pathlib import Path

def is_valid_java_project(project_path: str):
    """
    Checks whether the extracted project is a valid Java project.
    """

    project = Path(project_path)

    # Common Java project indicators
    checks = [
        project / "pom.xml",
        project / "build.gradle",
        project / "build.gradle.kts",
        project / "src",
        project / "src/main/java"
    ]

    for item in checks:
        if item.exists():
            return True

    return False