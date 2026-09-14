import subprocess
from pathlib import Path

class MetricsService:

    @staticmethod
    def run_metrics(project_path: str):

        jar_path = Path(__file__).parent.parent / "tools" / "JavaMetricsEngine-1.0-SNAPSHOT.jar"

        process = subprocess.run(
            [
                "java",
                "-jar",
                str(jar_path),
                project_path
            ],
            capture_output=True,
            text=True
        )

        print(process.stdout)

        if process.returncode != 0:
            print(process.stderr)
            raise Exception("Java Metrics Engine failed.")

        return "metrics.csv"