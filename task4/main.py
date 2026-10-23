from src.data.load.data_loader import load_data
from src.data.process.data_processor import process_data
import pandas as pd
from src.ai.client import ask_ai
from src.ai.query import query

STORE_NUM = 1

data = process_data(load_data(STORE_NUM))
books_df = data["books"]
users_df = data["users"]
orders_df = data["orders"]

question = "select users with e-mails started with s or p"
print(ask_ai(question, data))
