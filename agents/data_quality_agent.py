import pandas as pd


class DataQualityAgent:

    def __init__(self):
        self.agent_name = "Data Quality Agent"

    # 1. Missing Values
    def analyze_missing_values(self, df):

        missing_values = df.isnull().sum()

        missing_percentage = (
            df.isnull().sum() / len(df) * 100
        )

        missing_report = pd.DataFrame({
            "Missing Count": missing_values,
            "Missing Percentage": missing_percentage
        })

        missing_report = missing_report[
            missing_report["Missing Count"] > 0
        ]

        return missing_report

    # 2. Duplicate Rows
    def analyze_duplicates(self, df):

        duplicate_count = df.duplicated().sum()

        duplicate_percentage = (
            duplicate_count / len(df) * 100
        )

        duplicate_report = {
            "Duplicate Rows": int(duplicate_count),
            "Duplicate Percentage": float(round(
                duplicate_percentage, 2
            ))
        }

        return duplicate_report

    # 3. Data Types
    def analyze_data_types(self, df):

        data_type_report = {
            "Numerical Columns": len(
                df.select_dtypes(include="number").columns
            ),

            "Categorical Columns": len(
                df.select_dtypes(include="object").columns
            ),

            "DateTime Columns": len(
                df.select_dtypes(include="datetime").columns
            ),

            "Total Columns": len(df.columns)
        }

        return data_type_report

    # 4. Empty Strings
    def analyze_empty_strings(self, df):

        empty_string_report = {}

        for column in df.select_dtypes(include="object").columns:

            empty_count = (
                df[column]
                .str.strip()
                .eq("")
                .sum()
            )

            if empty_count > 0:

                empty_string_report[column] = int(
                    empty_count
                )

        return empty_string_report

    # 5. Constant Columns
    def analyze_constant_columns(self, df):

        constant_columns = []

        for column in df.columns:

            unique_values = df[column].nunique(
                dropna=False
            )

            if unique_values == 1:

                constant_columns.append(column)

        return constant_columns

    # 6. Complete Quality Analysis
    def run_quality_analysis(self, df):

        quality_report = {

            "Missing Values": self.analyze_missing_values(df),

            "Duplicate Analysis": self.analyze_duplicates(df),

            "Data Type Analysis": self.analyze_data_types(df),

            "Empty String Analysis": self.analyze_empty_strings(df),

            "Constant Columns": self.analyze_constant_columns(df),

            "Data Quality Score": self.calculate_quality_score(df)

        }

        return quality_report

    # 7. Quality Score
    def calculate_quality_score(self, df):

        total_cells = df.shape[0] * df.shape[1]

        if total_cells == 0:
            return 0

        missing_cells = df.isnull().sum().sum()

        duplicate_rows = df.duplicated().sum()

        empty_string_cells = 0

        for column in df.select_dtypes(include="object").columns:

            empty_string_cells += (
                df[column]
                .str.strip()
                .eq("")
                .sum()
            )

        problematic_cells = (
            missing_cells
            + duplicate_rows * df.shape[1]
            + empty_string_cells
        )

        quality_score = (
            1 - problematic_cells / total_cells
        ) * 100

        quality_score = max(
            0,
            round(quality_score, 2)
        )

        return float(quality_score)

    # 8. Quality Rating
    def get_quality_rating(self, score):

        if score >= 90:
            return "Excellent"

        elif score >= 75:
            return "Good"

        elif score >= 50:
            return "Moderate"

        else:
            return "Poor"

    # 9. Quality Explanation
    def get_quality_explanation(self, score):

        if score >= 90:
            return (
                "Your dataset is in excellent condition "
                "with very few data quality issues."
            )

        elif score >= 75:
            return (
                "Your dataset is in good condition, "
                "but some improvements may be needed."
            )

        elif score >= 50:
            return (
                "Your dataset has moderate data quality issues "
                "that should be addressed before analysis."
            )

        else:
            return (
                "Your dataset has significant data quality issues "
                "and requires cleaning before analysis."
            )

    # 10. Severity Classification
    def classify_severity(self, issue_type, percentage=0):

        if issue_type == "constant_columns":
            return "Info"

        if percentage < 1:
            return "Info"

        elif percentage <= 10:
            return "Warning"

        else:
            return "Critical"

    # 11. Recommendations
    def generate_recommendations(self, df):

        recommendations = []

               # Missing Values
        missing_values = df.isnull().sum()

        for column, count in missing_values.items():

            if count > 0:

                missing_percentage = (
                    count / len(df) * 100
                )

                severity = self.classify_severity(
                    "missing_values",
                    missing_percentage
                )

                                # Context Analysis
                missing_rows = df[df[column].isnull()]

                context_columns = []

                numerical_columns = df.select_dtypes(
                    include="number"
                ).columns.tolist()

                # Prioritize meaningful duration-related columns
                priority_keywords = [
                    "tenure",
                    "duration",
                    "month",
                    "year",
                    "time"
                ]

                numerical_columns.sort(
                    key=lambda col: any(
                        keyword in col.lower()
                        for keyword in priority_keywords
                    ),
                    reverse=True
                )

                for numerical_column in numerical_columns:

                    if numerical_column == column:
                        continue

                    values = missing_rows[numerical_column]

                    if (
                        not values.isnull().any()
                        and (values == 0).all()
                    ):

                        context_columns.append(
                            numerical_column
                        )

                context_message = ""

                if context_columns:

                    context_message = (
                        f" All rows with missing '{column}' "
                        f"have 0 in the following numerical "
                        f"columns: {', '.join(context_columns)}. "
                        "This may indicate a meaningful pattern "
                        "rather than random missing data."
                    )

                recommendations.append({
                    "severity": severity,
                    "issue": "Missing Values",
                    "recommendation": (
                        f"'{column}' contains {count} missing values "
                        f"({missing_percentage:.2f}% of rows). "
                        "Investigate the cause before deciding whether "
                        "to impute or remove them."
                        + context_message
                    )
                })

        # Duplicate Rows
        duplicate_count = df.duplicated().sum()

        if duplicate_count > 0:

            duplicate_percentage = (
                duplicate_count / len(df) * 100
            )

            severity = self.classify_severity(
                "duplicates",
                duplicate_percentage
            )

            recommendations.append({
                "severity": severity,
                "issue": "Duplicate Rows",
                "recommendation": (
                    f"The dataset contains {duplicate_count} duplicate rows "
                    f"({duplicate_percentage:.2f}% of rows). "
                    "Review them and remove duplicates if appropriate."
                )
            })

        # Empty Strings
        for column in df.select_dtypes(include="object").columns:

            empty_count = (
                df[column]
                .str.strip()
                .eq("")
                .sum()
            )

            if empty_count > 0:

                empty_percentage = (
                    empty_count / len(df) * 100
                )

                severity = self.classify_severity(
                    "empty_strings",
                    empty_percentage
                )

                recommendations.append({
                    "severity": severity,
                    "issue": "Empty Strings",
                    "recommendation": (
                        f"'{column}' contains {empty_count} empty strings "
                        f"({empty_percentage:.2f}% of rows). "
                        "Consider replacing them with missing values "
                        "or handling them appropriately."
                    )
                })

        # Constant Columns
        constant_columns = self.analyze_constant_columns(df)

        for column in constant_columns:

            severity = self.classify_severity(
                "constant_columns"
            )

            recommendations.append({
                "severity": severity,
                "issue": "Constant Column",
                "recommendation": (
                    f"'{column}' contains only one unique value. "
                    "Consider whether this column is useful for analysis."
                )
            })

        # No Issues Detected
        if not recommendations:

            recommendations.append({
                "severity": "Info",
                "issue": "Data Quality",
                "recommendation": (
                    "No major data quality issues detected. "
                    "The dataset appears ready for analysis."
                )
            })

        return recommendations

    def generate_quality_summary(self, df):

        quality_score = self.calculate_quality_score(df)

        quality_rating = self.get_quality_rating(
            quality_score
        )

        missing_count = int(
            df.isnull().sum().sum()
        )

        duplicate_count = int(
            df.duplicated().sum()
        )

        empty_string_count = 0

        for column in df.select_dtypes(include="object").columns:

            empty_string_count += (
                df[column]
                .str.strip()
                .eq("")
                .sum()
            )

        constant_columns = self.analyze_constant_columns(df)

        summary = {
            "Agent": self.agent_name,
            "Quality Score": quality_score,
            "Quality Rating": quality_rating,
            "Missing Values": missing_count,
            "Duplicate Rows": int(duplicate_count),
            "Empty Strings": int(empty_string_count),
            "Constant Columns": len(constant_columns),
            "Total Rows": int(len(df)),
            "Total Columns": int(len(df.columns))
        }

        return summary