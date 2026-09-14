class ImpactService:

    @staticmethod
    def calculate_impact(feature_vectors):

        results = []

        for item in feature_vectors:

            # ==========================================
            # 1. Read CK Metrics
            # ==========================================

            wmc = float(
                item.get("WMC", 0)
            )

            cbo = float(
                item.get("CBO", 0)
            )

            rfc = float(
                item.get("RFC", 0)
            )

            lcom = float(
                item.get("LCOM", 0)
            )

            # ==========================================
            # 2. Read SonarQube Metrics
            # ==========================================

            code_smells = float(
                item.get("Code Smells", 0)
            )

            vulnerabilities = float(
                item.get("Vulnerabilities", 0)
            )

            bugs = float(
                item.get("Bugs", 0)
            )

            major_issues = float(
                item.get("Major Issues", 0)
            )

            minor_issues = float(
                item.get("Minor Issues", 0)
            )

            blocker_issues = float(
                item.get("Blocker Issues", 0)
            )

            # ==========================================
            # 3. Calculate Impact Components
            # ==========================================

            # ------------------------------------------
            # Complexity
            # Maximum = 10
            # ------------------------------------------

            complexity_score = min(
                (wmc / 50) * 10,
                10
            )

            # ------------------------------------------
            # Coupling
            # Maximum = 10
            # ------------------------------------------

            coupling_score = min(
                (cbo / 20) * 10,
                10
            )

            # ------------------------------------------
            # Communication / RFC
            # Maximum = 10
            # ------------------------------------------

            communication_score = min(
                (rfc / 100) * 10,
                10
            )

            # ------------------------------------------
            # Lack of Cohesion
            # Maximum = 5
            # ------------------------------------------

            cohesion_score = min(
                (lcom / 20) * 5,
                5
            )

            # ------------------------------------------
            # Code Smells
            # Maximum = 15
            # ------------------------------------------

            code_quality_score = min(
                (code_smells / 20) * 15,
                15
            )

            # ------------------------------------------
            # Vulnerabilities
            # Maximum = 16
            # ------------------------------------------

            vulnerability_score = min(
                vulnerabilities * 8,
                16
            )

            # ------------------------------------------
            # Bugs
            # Maximum = 10
            # ------------------------------------------

            bug_score = min(
                bugs * 5,
                10
            )

            # ------------------------------------------
            # Major Issues
            # Maximum = 10
            # ------------------------------------------

            major_issue_score = min(
                major_issues * 5,
                10
            )

            # ------------------------------------------
            # Minor Issues
            # Maximum = 4
            # ------------------------------------------

            minor_issue_score = min(
                minor_issues * 1,
                4
            )

            # ------------------------------------------
            # Blocker Issues
            # Maximum = 10
            # ------------------------------------------

            blocker_score = min(
                blocker_issues * 10,
                10
            )

            # ==========================================
            # 4. Calculate Total Impact Score
            # ==========================================

            impact_score = (

                complexity_score

                + coupling_score

                + communication_score

                + cohesion_score

                + code_quality_score

                + vulnerability_score

                + bug_score

                + major_issue_score

                + minor_issue_score

                + blocker_score

            )

            # ==========================================
            # 5. Keep Score Between 0 and 100
            # ==========================================

            impact_score = min(
                max(
                    impact_score,
                    0
                ),
                100
            )

            # ==========================================
            # 6. Determine Impact Level
            #
            # New thresholds:
            #
            # 0 - 9.99   = LOW
            # 10 - 19.99 = MEDIUM
            # 20+        = HIGH
            # ==========================================

            if impact_score >= 20:

                impact_level = "HIGH"

            elif impact_score >= 10:

                impact_level = "MEDIUM"

            else:

                impact_level = "LOW"

            # ==========================================
            # 7. Determine Expected Benefits
            # ==========================================

            benefits = []

            # ------------------------------------------
            # Complexity benefit
            # ------------------------------------------

            if wmc > 20:

                benefits.append(
                    "Reduced code complexity"
                )

            # ------------------------------------------
            # Coupling benefit
            # ------------------------------------------

            if cbo > 10:

                benefits.append(
                    "Reduced class coupling"
                )

            # ------------------------------------------
            # RFC benefit
            # ------------------------------------------

            if rfc > 50:

                benefits.append(
                    "Improved maintainability"
                )

            # ------------------------------------------
            # Cohesion benefit
            # ------------------------------------------

            if lcom > 10:

                benefits.append(
                    "Improved class cohesion"
                )

            # ------------------------------------------
            # Code smell benefit
            # ------------------------------------------

            if code_smells > 0:

                benefits.append(
                    "Reduced code smells"
                )

            # ------------------------------------------
            # Security benefit
            # ------------------------------------------

            if vulnerabilities > 0:

                benefits.append(
                    "Improved security"
                )

            # ------------------------------------------
            # Reliability benefit
            # ------------------------------------------

            if bugs > 0:

                benefits.append(
                    "Improved reliability"
                )

            # ------------------------------------------
            # Major issue benefit
            # ------------------------------------------

            if major_issues > 0:

                benefits.append(
                    "Improved code quality"
                )

            # ------------------------------------------
            # Minor issue benefit
            # ------------------------------------------

            if minor_issues > 0:

                benefits.append(
                    "Improved maintainability"
                )

            # ------------------------------------------
            # Blocker issue benefit
            # ------------------------------------------

            if blocker_issues > 0:

                benefits.append(
                    "Removal of critical issues"
                )

            # ==========================================
            # 8. Remove Duplicate Benefits
            # ==========================================

            benefits = list(
                dict.fromkeys(
                    benefits
                )
            )

            # ==========================================
            # 9. Default Benefit
            # ==========================================

            if not benefits:

                benefits.append(
                    "Minor maintainability improvement"
                )

            # ==========================================
            # 10. Create Final Result
            # ==========================================

            results.append({

                "Class": str(
                    item.get(
                        "Class",
                        "Unknown"
                    )
                ),

                "impact_score": round(
                    impact_score,
                    2
                ),

                "impact_level":
                    impact_level,

                "expected_benefits":
                    benefits

            })

        # ==========================================
        # 11. Return Results
        # ==========================================

        return results