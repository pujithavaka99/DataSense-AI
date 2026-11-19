
import sys
import json
import pandas as pd

from utils.data_loader import load_dataset
from utils.data_cleaner import clean_data
from utils.data_profiler import profile_data
from utils.data_quality import check_data_quality
from utils.missing_value_analyzer import investigate_missing_totalcharges
from utils.intelligence_report import generate_intelligence_report

from utils.data_insights import (
    calculate_churn_rate,
    analyze_churn_by_contract,
    identify_contract_risk,
    analyze_churn_by_tenure
)

from utils.visualizer import (
    plot_churn_by_tenure,
    plot_churn_by_contract
)

from utils.business_insight_generator import (
    generate_business_insights
)


# ============================================================
# 1. LOAD DATASET
# ============================================================

print("=" * 60)
print("DATASENSE AI - DATA INTELLIGENCE SYSTEM")
print("=" * 60)

data_path = "data/Telco-Customer-Churn.csv"

df = load_dataset(data_path)

if df is None:
    print("Dataset loading failed. Exiting program.")
    sys.exit()


# ============================================================
# 2. DATA CLEANING
# ============================================================

df = clean_data(df)


# ============================================================
# 3. DATA PROFILING
# ============================================================

profile_data(df)


# ============================================================
# 4. DATA QUALITY CHECKS
# ============================================================

quality_report = check_data_quality(df)


# ============================================================
# 5. AUTOMATED QUALITY SUMMARY
# ============================================================

print("\n--- AUTOMATED QUALITY SUMMARY ---")

total_missing = sum(
    quality_report["missing_values"].values()
)

total_duplicates = quality_report["duplicate_rows"]

total_empty_strings = sum(
    quality_report["empty_strings"].values()
)

total_whitespace = sum(
    quality_report["whitespace_values"].values()
)

print("Total Missing Values:", total_missing)
print("Total Duplicate Rows:", total_duplicates)
print("Total Empty Strings:", total_empty_strings)
print("Total Whitespace Values:", total_whitespace)


# ============================================================
# 6. IDENTIFY COLUMNS WITH MISSING VALUES
# ============================================================

print("\n--- COLUMNS WITH MISSING VALUES ---")

missing_columns = {
    column: count
    for column, count in quality_report["missing_values"].items()
    if count > 0
}

print(missing_columns)


# ============================================================
# 7. INVESTIGATE MISSING TOTALCHARGES
# ============================================================

missing_report = investigate_missing_totalcharges(df)


# ============================================================
# 8. ASSESS MISSING VALUES
# ============================================================

print("\n--- MISSING VALUE ASSESSMENT ---")

if missing_report["positive_tenure_missing"] == 0:

    print(
        "All missing TotalCharges values belong to "
        "customers with tenure = 0."
    )

    print(
        "These records appear to represent newly joined customers."
    )

    print(
        "Decision: Preserve these records and do not delete them."
    )

else:

    print(
        "Missing TotalCharges values exist for customers "
        "with positive tenure."
    )

    print(
        "Further investigation is required."
    )


# ============================================================
# 9. OVERALL DATA QUALITY STATUS
# ============================================================

print("\n--- OVERALL DATA QUALITY STATUS ---")

if (
    total_duplicates == 0
    and total_empty_strings == 0
    and total_whitespace == 0
    and missing_report["positive_tenure_missing"] == 0
):

    overall_status = "GOOD - REVIEWED"

else:

    overall_status = "REQUIRES ATTENTION"


print("Status:", overall_status)


# ============================================================
# 10. GENERATE STRUCTURED INTELLIGENCE REPORT
# ============================================================

intelligence_report = generate_intelligence_report(
    df,
    quality_report,
    missing_report,
    overall_status
)


# ============================================================
# 11. SAVE CLEANED DATASET
# ============================================================

print("\n--- SAVING CLEANED DATASET ---")

cleaned_data_path = "data/Telco-Customer-Churn-Cleaned.csv"

df.to_csv(
    cleaned_data_path,
    index=False
)

print("Cleaned dataset saved successfully!")


# ============================================================
# 12. VERIFY SAVED DATASET
# ============================================================

print("\n--- VERIFYING SAVED DATASET ---")

verified_df = pd.read_csv(cleaned_data_path)

print("Verified Dataset Shape:", verified_df.shape)

print(
    "Verified TotalCharges Data Type:",
    verified_df["TotalCharges"].dtype
)


# ============================================================
# 13. FINAL DATA QUALITY VERIFICATION
# ============================================================

print("\n--- FINAL DATA QUALITY VERIFICATION ---")

print("Dataset Shape:", df.shape)

print(
    "Total Missing Values:",
    df.isnull().sum().sum()
)

print(
    "Total Duplicate Rows:",
    df.duplicated().sum()
)


# ============================================================
# 14. OVERALL CUSTOMER CHURN ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER CHURN ANALYSIS")
print("=" * 60)

print("\n--- OVERALL CHURN INSIGHTS ---")

churn_insight = calculate_churn_rate(df)

print(
    "Total Customers:",
    churn_insight["total_customers"]
)

print(
    "Churned Customers:",
    churn_insight["churned_customers"]
)

print(
    "Churn Rate:",
    churn_insight["churn_rate_percentage"],
    "%"
)


# ============================================================
# 15. CHURN ANALYSIS BY CONTRACT
# ============================================================

print("\n--- CHURN ANALYSIS BY CONTRACT ---")

contract_insights = analyze_churn_by_contract(df)

print(contract_insights)


# ============================================================
# 16. AUTOMATIC CONTRACT RISK IDENTIFICATION
# ============================================================

print("\n--- AUTOMATIC CONTRACT RISK IDENTIFICATION ---")

contract_risk = identify_contract_risk(
    contract_insights
)

print(
    "Highest Risk Contract:",
    contract_risk["highest_risk_contract"]
)

print(
    "Highest Risk Churn Rate:",
    contract_risk["highest_risk_churn_rate"],
    "%"
)

print(
    "Lowest Risk Contract:",
    contract_risk["lowest_risk_contract"]
)

print(
    "Lowest Risk Churn Rate:",
    contract_risk["lowest_risk_churn_rate"],
    "%"
)

print(
    "Risk Gap:",
    contract_risk["risk_gap_percentage_points"],
    "percentage points"
)


# ============================================================
# 17. CHURN ANALYSIS BY TENURE
# ============================================================

print("\n--- CHURN ANALYSIS BY TENURE ---")

tenure_insights = analyze_churn_by_tenure(df)

print(tenure_insights)


# ============================================================
# 18. AUTOMATIC BUSINESS INSIGHT GENERATION
# ============================================================

print("\n--- AUTOMATIC BUSINESS INSIGHTS ---")

business_insights = generate_business_insights(
    churn_insight,
    contract_risk,
    contract_insights,
    tenure_insights
)

for insight in business_insights:
    print("-", insight)


# ============================================================
# 19. VISUALIZE CHURN BY CONTRACT
# ============================================================

print("\n--- GENERATING CONTRACT CHURN VISUALIZATION ---")

plot_churn_by_contract(contract_insights)


# ============================================================
# 20. VISUALIZE CHURN BY TENURE
# ============================================================

print("\n--- GENERATING TENURE CHURN VISUALIZATION ---")

plot_churn_by_tenure(tenure_insights)


# ============================================================
# 21. UPDATE INTELLIGENCE REPORT WITH BUSINESS INSIGHTS
# ============================================================

print("\n--- UPDATING INTELLIGENCE REPORT ---")

intelligence_report["business_insights"] = {

    "overall_churn": churn_insight,

    "churn_by_contract": contract_insights.to_dict(
        orient="index"
    ),

    "contract_risk_analysis": contract_risk,

    "churn_by_tenure": tenure_insights.to_dict(
        orient="index"
    ),

    "generated_insights": business_insights
}


# ============================================================
# 22. SAVE FINAL INTELLIGENCE REPORT
# ============================================================

with open(
    "reports/intelligence_report.json",
    "w"
) as file:

    json.dump(
        intelligence_report,
        file,
        indent=4
    )

print(
    "Intelligence report updated successfully!"
)


# ============================================================
# 23. FINAL SYSTEM SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DATASENSE AI - EXECUTION COMPLETED")
print("=" * 60)

print("Dataset:", df.shape)

print("Data Quality Status:", overall_status)

print(
    "Customer Churn Rate:",
    churn_insight["churn_rate_percentage"],
    "%"
)

print(
    "Highest Risk Contract:",
    contract_risk["highest_risk_contract"]
)

print(
    "Highest Contract Churn Rate:",
    contract_risk["highest_risk_churn_rate"],
    "%"
)

print("\nGenerated Files:")
print("- data/Telco-Customer-Churn-Cleaned.csv")
print("- reports/intelligence_report.json")

print("\nAll analysis completed successfully!")
