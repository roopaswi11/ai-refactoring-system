import subprocess


class SonarQubeService:

    @staticmethod
    def run_analysis(project_path: str):

        # ==========================================
        # SonarQube Scanner
        # ==========================================

        scanner = (
            r"C:\Users\roopa\Downloads"
            r"\sonar-scanner-cli-8.1.0.6389-windows-x64"
            r"\sonar-scanner-8.1.0.6389-windows-x64"
            r"\bin\sonar-scanner.bat"
        )

        # ==========================================
        # SonarQube Token
        # ==========================================

        token = (
            "squ_998ed372f43deea079f8ea0820ab7627ad69e105"
        )

        # ==========================================
        # SonarQube Project
        # ==========================================

        project_key = "AI-Refactoring-System"

        # ==========================================
        # Scanner Command
        # ==========================================

        command = [

            scanner,

            f"-Dsonar.projectKey={project_key}",

            f"-Dsonar.projectName={project_key}",

            f"-Dsonar.sources={project_path}",

            "-Dsonar.host.url=http://localhost:9000",

            f"-Dsonar.token={token}",

            "-Dsonar.java.binaries=."
        ]

        print(
            "\n========================================"
        )

        print(
            "Running SonarQube Analysis"
        )

        print(
            "Project:",
            project_key
        )

        print(
            "Source:",
            project_path
        )

        print(
            "========================================"
        )

        # ==========================================
        # Run SonarQube Scanner
        # ==========================================

        process = subprocess.run(

            command,

            capture_output=True,

            text=True
        )

        # ==========================================
        # Print Output
        # ==========================================

        print(
            "\n========== SONARQUBE STDOUT =========="
        )

        print(
            process.stdout
        )

        print(
            "\n========== SONARQUBE STDERR =========="
        )

        print(
            process.stderr
        )

        # ==========================================
        # Check Result
        # ==========================================

        if process.returncode != 0:

            raise Exception(
                "SonarQube analysis failed:\n"
                + process.stderr
            )

        print(
            "\nSonarQube analysis completed successfully."
        )

        return True