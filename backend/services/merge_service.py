class MergeService:

    @staticmethod
    def merge(metrics, issues):

        merged = []

        for metric in metrics:

            class_name = metric["Class"]

            class_issues = []

            for issue in issues:

                if class_name + ".java" in issue["file"]:

                    class_issues.append(issue)

            merged.append({

                "class": class_name,

                "wmc": int(metric["WMC"]),

                "cbo": int(metric["CBO"]),

                "dit": int(metric["DIT"]),

                "noc": int(metric["NOC"]),

                "rfc": int(metric["RFC"]),

                "lcom": int(metric["LCOM"]),

                "issues": class_issues

            })

        return merged