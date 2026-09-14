import requests
from pathlib import Path


class SonarResultsService:

    @staticmethod
    def get_results(project_path: str):

        # ==========================================
        # SonarQube Token
        # ==========================================

        token = (
            "sqp_de91c945287a016081e38767d93b7c555309ecd1"
        )

        # ==========================================
        # Existing SonarQube Project
        # ==========================================

        project_key = "AI-Refactoring-System"

        # ==========================================
        # SonarQube API
        # ==========================================

        url = (
            "http://localhost:9000/api/issues/search"
        )

        params = {
            "componentKeys": project_key,
            "ps": 500
        }

        # ==========================================
        # Request SonarQube
        # ==========================================

        response = requests.get(
            url,
            params=params,
            auth=(token, ""),
            timeout=30
        )

        # ==========================================
        # Check Response
        # ==========================================

        if response.status_code != 200:

            raise Exception(
                "SonarQube API failed.\n"
                f"Status: {response.status_code}\n"
                f"Response: {response.text}"
            )

        data = response.json()

        # ==========================================
        # Current project folder
        # ==========================================

        current_project = Path(
            project_path
        ).resolve()

        current_project_name = (
            current_project.name
        )

        print(
            "\nCurrent project:"
        )

        print(
            current_project_name
        )

        # ==========================================
        # Extract and filter issues
        # ==========================================

        issues = []

        for issue in data.get(
            "issues",
            []
        ):

            component = issue.get(
                "component",
                ""
            )

            # --------------------------------------
            # SonarQube component example:
            #
            # AI-Refactoring-System:
            # extracted_projects/LibraryManagementTestProject/
            # src/com/library/Book.java
            # --------------------------------------

            component_path = Path(
                component
            )

            component_string = str(
                component_path
            ).replace(
                "\\",
                "/"
            )

            project_name_lower = (
                current_project_name.lower()
            )

            # --------------------------------------
            # Keep only issues belonging to the
            # current uploaded project
            # --------------------------------------

            if project_name_lower not in (
                component_string.lower()
            ):

                continue

            issues.append({

                "file": component,

                "line": issue.get(
                    "line"
                ),

                "severity": issue.get(
                    "severity",
                    ""
                ),

                "type": issue.get(
                    "type",
                    ""
                ),

                "message": issue.get(
                    "message",
                    ""
                )
            })

        # ==========================================
        # Debug Information
        # ==========================================

        print(
            "\n========== SONARQUBE RESULTS =========="
        )

        print(
            "Project:",
            project_key
        )

        print(
            "Current upload:",
            current_project_name
        )

        print(
            "Total SonarQube issues:",
            len(data.get("issues", []))
        )

        print(
            "Issues belonging to current project:",
            len(issues)
        )

        for issue in issues:

            print(
                issue
            )

        print(
            "========================================"
        )

        return issues