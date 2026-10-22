from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data" / "raw"
FILE_NAMES = ("books.yaml", "users.csv", "orders.parquet")
STORE_NAME_TEMPLATE = "STORE{store_num}"
EXCHANGE_RATES = {"EUR" : "1.2", "USD" : "1.0"}
