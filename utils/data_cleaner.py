import pandas as pd


def clean_data(df):

    print("Starting data cleaning...")

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()

    # Handle TotalCharges only when the column exists
    if "TotalCharges" in df.columns:

        df["TotalCharges"] = pd.to_numeric(
            df["TotalCharges"].astype(str).str.strip(),
            errors="coerce"
        )

    # Clean string columns
    for column in df.select_dtypes(include="object").columns:

        df[column] = df[column].astype(str).str.strip()

    print("Data cleaning completed!")

    return df