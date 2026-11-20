import pandas as pd

class DataAnalystAgent:

    def __init__(self):
        self.agent_name = "Data Analyst Agent"
    def analyze_numerical_data(self, df):

        numerical_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if not numerical_columns:

            return "No numerical columns found in the dataset."

        numerical_analysis = {}

        for column in numerical_columns:

            numerical_analysis[column] = {
                "Count": int(df[column].count()),
                "Mean": float(df[column].mean()),
                "Median": float(df[column].median()),
                "Standard Deviation": float(df[column].std()),
                "Minimum": float(df[column].min()),
                "Maximum": float(df[column].max()),
                "25th Percentile": float(
                    df[column].quantile(0.25)
                ),
                "75th Percentile": float(
                    df[column].quantile(0.75)
                ),
                "Skewness": float(df[column].skew())
            }

        return numerical_analysis        

    def analyze_categorical_data(self, df):

        categorical_columns = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        if not categorical_columns:

            return "No categorical columns found in the dataset."

        categorical_analysis = {}

        for column in categorical_columns:

            value_counts = df[column].value_counts()
            unique_values = int(df[column].nunique())

            if value_counts.empty:

                most_frequent_value = None
                most_frequent_count = 0
                value_distribution = {}

            else:

                most_frequent_value = str(value_counts.index[0])
                most_frequent_count = int(value_counts.iloc[0])
                value_distribution = value_counts.to_dict()

            categorical_analysis[column] = {
                "Unique Values": unique_values,
                "Most Frequent Value": most_frequent_value,
                "Most Frequent Count": most_frequent_count,
                "Value Distribution": value_distribution
            }

        return categorical_analysis

    def analyze_outliers(self, df):

        numerical_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if not numerical_columns:

            return "No numerical columns found."

        outlier_analysis = {}

        for column in numerical_columns:

            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)

            IQR = Q3 - Q1

            lower_bound = Q1 - (1.5 * IQR)
            upper_bound = Q3 + (1.5 * IQR)

            outliers = df[
                (df[column] < lower_bound) |
                (df[column] > upper_bound)
            ][column]

            outlier_analysis[column] = {
                "Q1": float(Q1),
                "Q3": float(Q3),
                "IQR": float(IQR),
                "Lower Bound": float(lower_bound),
                "Upper Bound": float(upper_bound),
                "Outlier Count": int(len(outliers)),
                "Outlier Values": outliers.tolist()
            }

        return outlier_analysis

    def analyze_correlations(self, df):

        numerical_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if len(numerical_columns) < 2:

            return "At least two numerical columns are required."

        correlation_matrix = df[numerical_columns].corr()

        correlation_analysis = {}

        for i in range(len(numerical_columns)):

            for j in range(i + 1, len(numerical_columns)):

                column1 = numerical_columns[i]
                column2 = numerical_columns[j]

                correlation = correlation_matrix.loc[
                    column1, column2
                ]

                if pd.isna(correlation):

                    continue

                correlation = float(correlation)

                absolute_correlation = abs(correlation)


                # Correlation Strength
                if absolute_correlation >= 0.7:

                    strength = "Strong"

                elif absolute_correlation >= 0.4:

                    strength = "Moderate"

                elif absolute_correlation >= 0.2:

                    strength = "Weak"

                else:

                    strength = "Very Weak"


                # Correlation Direction
                if correlation > 0:

                    direction = "Positive"

                    explanation = (
                        f"As {column1} increases, {column2} "
                        f"tends to increase."
                    )

                elif correlation < 0:

                    direction = "Negative"

                    explanation = (
                        f"As {column1} increases, {column2} "
                        f"tends to decrease."
                    )

                else:

                    direction = "No Correlation"

                    explanation = (
                        f"No linear relationship was detected "
                        f"between {column1} and {column2}."
                    )


                correlation_analysis[
                    f"{column1} vs {column2}"
                ] = {

                    "Correlation": round(correlation, 3),

                    "Strength": strength,

                    "Direction": direction,

                    "Interpretation": explanation

                }


        return correlation_analysis

    def generate_statistical_insights(self, df):

        insights = []

        numerical_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()


        # Numerical Insights
        for column in numerical_columns:

            values = df[column].dropna()

            if values.empty:

                insights.append(
                    f"{column}: No valid numerical values available for analysis."
                )

                continue

            mean_value = values.mean()
            median_value = values.median()
            skewness = values.skew()
            standard_deviation = values.std()
            data_range = values.max() - values.min()


            insights.append(
                f"{column}: Average is {mean_value:.2f}, "
                f"median is {median_value:.2f}."
            )

            insights.append(
                f"{column}: Standard deviation is "
                f"{standard_deviation:.2f}, and range is "
                f"{data_range:.2f}."
            )


            # Distribution Insights
            if pd.isna(skewness):

                insights.append(
                    f"{column}: Distribution cannot be determined."
                )

            elif skewness > 0.5:

                insights.append(
                    f"{column} is positively skewed "
                    "(right-skewed)."
                )

            elif skewness < -0.5:

                insights.append(
                    f"{column} is negatively skewed "
                    "(left-skewed)."
                )

            else:

                insights.append(
                    f"{column} is approximately symmetrical."
                )


            # Variability Insights
            if mean_value != 0:

                coefficient_of_variation = (
                    standard_deviation / abs(mean_value)
                ) * 100

                if coefficient_of_variation < 15:

                    insights.append(
                        f"{column} has relatively low variability."
                    )

                elif coefficient_of_variation < 50:

                    insights.append(
                        f"{column} has moderate variability."
                    )

                else:

                    insights.append(
                        f"{column} has high variability."
                    )


        # Categorical Insights
        for column in categorical_columns:

            value_counts = df[column].value_counts()

            if not value_counts.empty:

                most_frequent = value_counts.index[0]
                frequency = value_counts.iloc[0]

                insights.append(
                    f"{column}: Most frequent category is "
                    f"{most_frequent} ({frequency} records)."
                )


        return insights

    def generate_key_findings(self, df, analysis_results):

        findings = []

        # Correlation Findings
        correlations = analysis_results["Correlation Analysis"]

        if isinstance(correlations, dict) and correlations:

            strongest_correlation = max(
                correlations.items(),
                key=lambda item: abs(item[1]["Correlation"])
            )

            pair = strongest_correlation[0]
            details = strongest_correlation[1]

            findings.append(
                f"{pair} has the strongest correlation "
                f"({details['Correlation']}) with "
                f"{details['Direction'].lower()} direction."
            )


        # Outlier Findings
        outliers = analysis_results["Outlier Analysis"]

        if isinstance(outliers, dict):

            for column, details in outliers.items():

                if details["Outlier Count"] > 0:

                    findings.append(
                        f"{column} contains "
                        f"{details['Outlier Count']} outlier(s)."
                    )


        # Variability Findings
        numerical_analysis = analysis_results["Numerical Analysis"]

        if isinstance(numerical_analysis, dict):

            for column, details in numerical_analysis.items():

                mean_value = details["Mean"]
                std_value = details["Standard Deviation"]

                if mean_value != 0:

                    cv = (std_value / abs(mean_value)) * 100

                    if cv >= 50:

                        findings.append(
                            f"{column} shows high variability "
                            f"relative to its average."
                        )


        # Skewness Findings
        if isinstance(numerical_analysis, dict):

            for column, details in numerical_analysis.items():

                skewness = details["Skewness"]

                if skewness > 0.5:

                    findings.append(
                        f"{column} has a right-skewed distribution."
                    )

                elif skewness < -0.5:

                    findings.append(
                        f"{column} has a left-skewed distribution."
                    )


        # Categorical Findings
        categorical_analysis = analysis_results[
            "Categorical Analysis"
        ]

        if isinstance(categorical_analysis, dict):

            for column, details in categorical_analysis.items():

                if details["Most Frequent Value"] is not None:

                    findings.append(
                        f"{column}'s most common category is "
                        f"{details['Most Frequent Value']}."
                    )


        if not findings:

            findings.append(
                "No significant patterns were identified "
                "in the available dataset."
            )


        return findings
    
    def run_analysis(self, df):

        if df.empty:

            return {
                "Error": "The dataset is empty. Please upload a dataset containing rows."
            }

        analysis_results = {

            "Numerical Analysis": self.analyze_numerical_data(df),

            "Categorical Analysis": self.analyze_categorical_data(df),

            "Outlier Analysis": self.analyze_outliers(df),

            "Correlation Analysis": self.analyze_correlations(df),

            "Statistical Insights": self.generate_statistical_insights(df)

        }

        analysis_results["Key Findings"] = self.generate_key_findings(
            df,
            analysis_results
        )

        return analysis_results