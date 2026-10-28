import pandas as pd

def clean_data(df):
    return df.dropna(axis="columns", how="all")