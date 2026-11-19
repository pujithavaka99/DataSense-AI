def investigate_missing_totalcharges(df):

    missing_totalcharges = df[df["TotalCharges"].isnull()]

    zero_tenure_missing = missing_totalcharges[
        missing_totalcharges["tenure"] == 0
    ]

    positive_tenure_missing = missing_totalcharges[
        missing_totalcharges["tenure"] > 0
    ]

    investigation_report = {
        "total_missing": len(missing_totalcharges),
        "zero_tenure_missing": len(zero_tenure_missing),
        "positive_tenure_missing": len(positive_tenure_missing)
    }

    print("\n--- MISSING VALUE INVESTIGATION ---")

    print("Records with missing TotalCharges:",
          investigation_report["total_missing"])

    print("Missing TotalCharges with tenure = 0:",
          investigation_report["zero_tenure_missing"])

    print("Missing TotalCharges with tenure > 0:",
          investigation_report["positive_tenure_missing"])

    return investigation_report