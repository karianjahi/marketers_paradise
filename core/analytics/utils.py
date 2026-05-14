import pandas as pd
def read_csv(file):
    return pd.read_csv(file)

def get_missing_columns(df, cols):
    return [col for col in cols if col not in df.columns]

def is_row_valid(row, colnames):
    return not row[colnames].isnull().any()


        