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

# question = "which customer spends the most money and what are there user_ids list?"
# print(ask_ai(question, data))

print(list(books_df['genre'].unique()))