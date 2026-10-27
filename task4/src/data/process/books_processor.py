import pandas as pd

def normalize_authors(df):
    df["author_set"] = df["author"].apply(lambda authors: tuple(sorted(author.strip() for author in authors.split(","))))
    df["number_of_authors"] = df["author_set"].apply(lambda a_set: len(a_set))

def process_years(df):
    df["year"] = df["year"].replace(["-1", "0"], pd.NA)
    df["year"] = pd.to_numeric(df["year"]).astype("Int64")

def process(df):
    normalize_authors(df)
    process_years(df)
