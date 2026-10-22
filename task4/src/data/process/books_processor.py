import pandas as pd

def process(df):
    df["year"] = df["year"].astype("Int64")
