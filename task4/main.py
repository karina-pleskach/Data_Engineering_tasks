from src.data.load.data_loader import load_data
from src.data.process.data_processor import process_data
import pandas as pd

STORE_NUM = 1

data = process_data(load_data(STORE_NUM))
books_df = data["books"]
users_df = data["users"]
orders_df = data["orders"]
