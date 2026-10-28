import pandas as pd
from src.data.process.data_cleaner import clean_data

def process_date(df):
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df

def set_date_index(df):
    return df.set_index("Date")

def process_data(df):
    df = clean_data(df)
    return set_date_index(process_date(df))
