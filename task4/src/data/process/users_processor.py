def process(df):
    df["phone"] = df["phone"].str.replace(r"\s+|\.+|\(+|\)+|\-+", "", regex=True)
