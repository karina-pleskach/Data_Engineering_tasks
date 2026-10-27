from pathlib import Path
import pandas as pd
import yaml

def read_yaml(file_path):
    with open(file_path, encoding="utf-8") as file:
        return pd.DataFrame(yaml.safe_load(file))

pd.read_yaml = read_yaml

def read(file_path):
    extension = Path(file_path).suffix.lower()[1:]
    return getattr(pd, f"read_{extension}")(file_path)
