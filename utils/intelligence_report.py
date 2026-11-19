def generate_intelligence_report(
    df,
    quality_report,
    missing_report,
    overall_status
):

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


    report = {

        "dataset": {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1])
        },

        "quality": {
            "missing_values": int(total_missing),
            "duplicate_rows": int(total_duplicates),
            "empty_strings": int(total_empty_strings),
            "whitespace_values": int(total_whitespace)
        },

        "missing_value_investigation": {
            "TotalCharges": {
                "missing": int(missing_report["total_missing"]),
                "zero_tenure": int(
                    missing_report["zero_tenure_missing"]
                ),
                "positive_tenure": int(
                    missing_report["positive_tenure_missing"]
                )
            }
        },

        "overall_status": overall_status
    }

    return report