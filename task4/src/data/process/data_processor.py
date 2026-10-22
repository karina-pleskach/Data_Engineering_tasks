from importlib import import_module
from src.data.process.data_cleaner import clean_df

def process_data(data):
    for name, df in data.items():
        clean_df(df)
        import_module(f"{__package__}.{name}_processor").process(df)
    return data
