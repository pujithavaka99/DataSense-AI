class BusinessIntelligenceAgent:

    def __init__(self):

        self.agent_name = "Business Intelligence Agent"

        self.description = (
            "Analyzes datasets from a business perspective "
            "and generates KPIs, performance insights, "
            "risks, and actionable recommendations."
        )
    def identify_business_kpis(self, df):

        kpi_candidates = []

        numerical_columns = df.select_dtypes(
            include="number"
        ).columns

        business_keywords = [
            "revenue",
            "sales",
            "profit",
            "income",
            "cost",
            "expense",
            "price",
            "amount",
            "salary",
            "balance",
            "payment",
            "charge",
            "quantity",
            "count",
            "orders",
            "churn",
            "rating",
            "score"
        ]

        identifier_keywords = [
            "id",
            "customerid",
            "userid",
            "accountid",
            "employeeid",
            "productid",
            "orderid",
            "transactionid",
            "subscriptionid"
        ]

        for column in numerical_columns:

            column_name = column.lower().replace(
                "_", ""
            ).replace(" ", "")

            # Skip identifier columns

            if any(
                identifier in column_name
                for identifier in identifier_keywords
            ):

                continue

            # Identify potential business metrics

            for keyword in business_keywords:

                if keyword in column_name:

                    kpi_candidates.append({
                        "KPI": column,
                        "Category": "Business Metric",
                        "Reason": (
                            f"Column '{column}' may represent "
                            f"a business metric related to "
                            f"{keyword}."
                        )
                    })

                    break

        return kpi_candidates
    
    def calculate_kpi_summary(self, df, kpi_candidates):

        kpi_summary = []

        for kpi in kpi_candidates:

            column = kpi["KPI"]

            values = df[column].dropna()

            summary = {
                "KPI": column,
                "Count": len(values),
                "Total": values.sum(),
                "Average": values.mean(),
                "Minimum": values.min(),
                "Maximum": values.max()
            }

            kpi_summary.append(summary)

        return kpi_summary
    

    def generate_kpi_insights(self, kpi_summary):

        insights = []

        for kpi in kpi_summary:

            name = kpi["KPI"]

            total = kpi["Total"]

            average = kpi["Average"]

            maximum = kpi["Maximum"]

            minimum = kpi["Minimum"]

            insights.append(
                f"{name}: Total value is {total:,.2f}, "
                f"with an average of {average:,.2f}. "
                f"The values range from {minimum:,.2f} "
                f"to {maximum:,.2f}."
            )

        return insights

    def identify_kpi_performance(self, kpi_summary):

        performance_insights = []

        if not kpi_summary:
            return performance_insights

        highest_kpi = max(
            kpi_summary,
            key=lambda x: x["Total"]
        )

        lowest_kpi = min(
            kpi_summary,
            key=lambda x: x["Total"]
        )

        performance_insights.append(
            f"{highest_kpi['KPI']} has the highest "
            f"total value of {highest_kpi['Total']:,.2f}."
        )

        performance_insights.append(
            f"{lowest_kpi['KPI']} has the lowest "
            f"total value of {lowest_kpi['Total']:,.2f}."
        )

        return performance_insights

    def analyze_kpi_variation(self, kpi_summary):

        variation_insights = []

        for kpi in kpi_summary:

            name = kpi["KPI"]
            average = kpi["Average"]
            maximum = kpi["Maximum"]
            minimum = kpi["Minimum"]

            variation = maximum - minimum

            if average != 0:
                variation_percentage = (
                    variation / abs(average)
                ) * 100
            else:
                variation_percentage = 0

            if variation_percentage >= 50:
                level = "High Variation"

            elif variation_percentage >= 20:
                level = "Moderate Variation"

            else:
                level = "Low Variation"

            variation_insights.append({
                "KPI": name,
                "Range": variation,
                "Variation Percentage": variation_percentage,
                "Variation Level": level
            })

        return variation_insights

    def generate_business_recommendations(self, variation_insights):

        recommendations = []

        for insight in variation_insights:

            kpi = insight["KPI"]
            variation_level = insight["Variation Level"]

            if variation_level == "High Variation":

                recommendations.append(
                    f"{kpi} shows high variation. "
                    f"Investigate the factors causing differences "
                    f"and identify opportunities to improve consistency."
                )

            elif variation_level == "Moderate Variation":

                recommendations.append(
                    f"{kpi} shows moderate variation. "
                    f"Monitor this metric regularly and identify "
                    f"potential improvement opportunities."
                )

            else:

                recommendations.append(
                    f"{kpi} shows low variation. "
                    f"Continue monitoring to maintain consistency."
                )

        return recommendations
    
    def calculate_profit_margin(self, df):

        revenue_columns = [
            column for column in df.columns
            if "revenue" in column.lower()
        ]

        profit_columns = [
            column for column in df.columns
            if "profit" in column.lower()
        ]

        if not revenue_columns or not profit_columns:
            return None

        revenue_column = revenue_columns[0]
        profit_column = profit_columns[0]

        total_revenue = df[revenue_column].sum()
        total_profit = df[profit_column].sum()

        if total_revenue == 0:
            return None

        profit_margin = (
            total_profit / total_revenue
        ) * 100

        return {
            "Total Revenue": total_revenue,
            "Total Profit": total_profit,
            "Profit Margin (%)": profit_margin
        }

    def analyze_kpi_by_category(
        self,
        df,
        category_column,
        kpi_column
    ):

        if category_column not in df.columns:
            return None

        if kpi_column not in df.columns:
            return None

        grouped_analysis = df.groupby(
            category_column
        )[kpi_column].agg([
            "count",
            "sum",
            "mean",
            "min",
            "max"
        ])

        return grouped_analysis
    
    def generate_category_insights(
        self,
        grouped_analysis,
        kpi_column
    ):

        if grouped_analysis is None or grouped_analysis.empty:
            return []

        insights = []

        highest_category = grouped_analysis["sum"].idxmax()
        lowest_category = grouped_analysis["sum"].idxmin()

        highest_value = grouped_analysis.loc[
            highest_category, "sum"
        ]

        lowest_value = grouped_analysis.loc[
            lowest_category, "sum"
        ]

        insights.append(
            f"{highest_category} has the highest total "
            f"{kpi_column} with {highest_value:,.2f}."
        )

        insights.append(
            f"{lowest_category} has the lowest total "
            f"{kpi_column} with {lowest_value:,.2f}."
        )

        return insights

    def calculate_category_contribution(
        self,
        grouped_analysis
    ):

        if grouped_analysis is None or grouped_analysis.empty:
            return None

        total_value = grouped_analysis["sum"].sum()

        if total_value == 0:
            return None

        contribution = (
            grouped_analysis["sum"] / total_value
        ) * 100

        contribution = contribution.sort_values(
            ascending=False
        )

        return contribution

    def generate_contribution_insights(
        self,
        category_contribution,
        kpi_column
    ):

        if category_contribution is None:
            return []

        insights = []

        highest_category = category_contribution.index[0]
        highest_percentage = category_contribution.iloc[0]

        lowest_category = category_contribution.index[-1]
        lowest_percentage = category_contribution.iloc[-1]

        insights.append(
            f"{highest_category} contributes the highest share "
            f"of total {kpi_column} at "
            f"{highest_percentage:.2f}%."
        )

        insights.append(
            f"{lowest_category} contributes the lowest share "
            f"of total {kpi_column} at "
            f"{lowest_percentage:.2f}%."
        )

        return insights