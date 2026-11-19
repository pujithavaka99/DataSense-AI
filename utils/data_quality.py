def check_data_quality(df):

    print("\n--- MISSING VALUES CHECK ---")

    missing_values = df.isnull().sum()
    print(missing_values)


    print("\n--- DUPLICATE ROWS CHECK ---")

    duplicate_rows = df.duplicated().sum()
    print("Duplicate rows:", duplicate_rows)


    print("\n--- EMPTY STRING CHECK ---")

    empty_strings = (df == "").sum()
    print(empty_strings)


    print("\n--- WHITESPACE CHECK ---")

    whitespace_values = df.apply(
        lambda column: column.astype(str).str.strip().eq("").sum()
    )

    print(whitespace_values)


    # Collect all results into a dictionary
    quality_report = {
        "missing_values": missing_values.to_dict(),
        "duplicate_rows": int(duplicate_rows),
        "empty_strings": empty_strings.to_dict(),
        "whitespace_values": whitespace_values.to_dict()
    }

    return quality_report