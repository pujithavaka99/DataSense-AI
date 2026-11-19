import pandas as pd


def load_dataset(file_path):
    try:
        df = pd.read_csv(file_path)

        print("Dataset loaded successfully!")
        return df

    except FileNotFoundError:
        print("Error: File not found!")
        return None