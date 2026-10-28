import pandas as pd

def load_data(url):
    return pd.read_csv(url, on_bad_lines='skip')
