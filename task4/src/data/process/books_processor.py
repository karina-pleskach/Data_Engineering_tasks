import pandas as pd

def normalize_authors(df):
    df["author_set"] = df["author"].apply(lambda authors: tuple(sorted(author.strip() for author in authors.split(","))))

def process(df):
    normalize_authors(df)
    df["year"] = pd.to_numeric(df["year"]).astype("Int64")
