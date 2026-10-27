import re
import pandas as pd

COLUMN_NAME_PATTERN = re.compile(r"\W+")

def rename_columns(df):
    df.rename({c : COLUMN_NAME_PATTERN.sub("", c) for c in df.columns}, axis="columns", inplace=True)

def trim_values(df):
    df.replace(r"^\s+|\s+$", "", regex=True, inplace=True)

def process_missing_values(df):
    df.replace(["-", "NULL", "", None], pd.NA, inplace=True)

def remove_duplicates(df):
    df.drop_duplicates(subset=["id"], keep="first", inplace=True)

def clean_df(df):
    rename_columns(df)
    trim_values(df)
    process_missing_values(df)
    remove_duplicates(df)
