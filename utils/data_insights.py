import pandas as pd
def calculate_churn_rate(df):

    total_customers = len(df)

    churned_customers = (df["Churn"] == "Yes").sum()

    churn_rate = (
        churned_customers / total_customers
    ) * 100

    insight = {
        "total_customers": int(total_customers),
        "churned_customers": int(churned_customers),
        "churn_rate_percentage": round(churn_rate, 2)
    }

    return insight

def analyze_churn_by_contract(df):

    contract_analysis = df.groupby("Contract").agg(
        total_customers=("customerID", "count"),
        churned_customers=("Churn", lambda x: (x == "Yes").sum())
    )

    contract_analysis["churn_rate"] = (
        contract_analysis["churned_customers"]
        / contract_analysis["total_customers"]
    ) * 100

    contract_analysis["churn_rate"] = (
        contract_analysis["churn_rate"].round(2)
    )

    return contract_analysis

def identify_contract_risk(contract_analysis):

    highest_risk_contract = contract_analysis[
        "churn_rate"
    ].idxmax()

    highest_risk_rate = contract_analysis.loc[
        highest_risk_contract,
        "churn_rate"
    ]

    lowest_risk_contract = contract_analysis[
        "churn_rate"
    ].idxmin()

    lowest_risk_rate = contract_analysis.loc[
        lowest_risk_contract,
        "churn_rate"
    ]

    risk_gap = round(
        highest_risk_rate - lowest_risk_rate,
        2
    )

    risk_insight = {
        "highest_risk_contract": highest_risk_contract,
        "highest_risk_churn_rate": float(highest_risk_rate),
        "lowest_risk_contract": lowest_risk_contract,
        "lowest_risk_churn_rate": float(lowest_risk_rate),
        "risk_gap_percentage_points": risk_gap
    }

    return risk_insight

def analyze_churn_by_tenure(df):

    df = df.copy()

    df["tenure_group"] = pd.cut(df["tenure"],
        bins=[-1, 12, 36, 72],
        labels=[
            "New customers",
            "Medium-term customers",
            "Long-term customers"
        ]
    )

    tenure_analysis = df.groupby(
        "tenure_group",
        observed=True
    ).agg(
        total_customers=("customerID", "count"),
        churned_customers=("Churn", lambda x: (x == "Yes").sum())
    )

    tenure_analysis["churn_rate"] = (
        tenure_analysis["churned_customers"]
        / tenure_analysis["total_customers"]
    ) * 100

    tenure_analysis["churn_rate"] = (
        tenure_analysis["churn_rate"].round(2)
    )

    return tenure_analysis