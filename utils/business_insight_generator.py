
def generate_business_insights(
    churn_insight,
    contract_risk,
    contract_analysis,
    tenure_analysis
):

    insights = []

    # Insight 1: Overall churn
    churn_rate = churn_insight["churn_rate_percentage"]

    insights.append(
        f"Overall customer churn rate is {churn_rate}%."
    )

    # Insight 2: Highest-risk contract
    highest_contract = contract_risk["highest_risk_contract"]
    highest_rate = contract_risk["highest_risk_churn_rate"]

    insights.append(
        f"{highest_contract} customers have the highest "
        f"churn rate at {highest_rate}%."
    )

    # Insight 3: Lowest-risk contract
    lowest_contract = contract_risk["lowest_risk_contract"]
    lowest_rate = contract_risk["lowest_risk_churn_rate"]

    insights.append(
        f"{lowest_contract} customers have the lowest "
        f"churn rate at {lowest_rate}%."
    )

    # Insight 4: Contract risk gap
    risk_gap = contract_risk["risk_gap_percentage_points"]

    insights.append(
        f"The churn rate difference between the highest-risk "
        f"and lowest-risk contract types is {risk_gap} "
        f"percentage points."
    )

    # Insight 5: Highest churn tenure group
    highest_tenure_group = tenure_analysis["churn_rate"].idxmax()

    highest_tenure_rate = tenure_analysis.loc[
        highest_tenure_group,
        "churn_rate"
    ]

    insights.append(
        f"{highest_tenure_group} have the highest churn "
        f"rate at {highest_tenure_rate}%."
    )

    # Insight 6: Lowest churn tenure group
    lowest_tenure_group = tenure_analysis["churn_rate"].idxmin()

    lowest_tenure_rate = tenure_analysis.loc[
        lowest_tenure_group,
        "churn_rate"
    ]

    insights.append(
        f"{lowest_tenure_group} have the lowest churn "
        f"rate at {lowest_tenure_rate}%."
    )

    return insights
