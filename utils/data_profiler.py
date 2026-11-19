def profile_data(df):

    print("\n--- DATASET PROFILE ---")

    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\n--- FIRST 5 ROWS ---")
    print(df.head())

    print("\n--- DETAILED DATASET INFORMATION ---")
    df.info()