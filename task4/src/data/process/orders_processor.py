import config
import re
import pandas as pd
from decimal import Decimal

def get_currency(value):
    return re.search(r"USD|EUR|\$|€", value).group(0)

def normalize_currency(currency):
    return {"$" : "USD", "€" : "EUR"}.get(currency, currency)

def get_price(value):
    match = re.search(r"(\d+)\D*(\d+)?", value)
    return Decimal(".".join((match.group(1), match.group(2) or "0")))

def convert_price(value):
    currency = normalize_currency(get_currency(value))
    return get_price(value) * Decimal(config.EXCHANGE_RATES[currency])

def convert_datetime(value):
    value = value.replace(";", " ").replace(",", " ")
    value = re.sub(r"\bA\.M\.", "AM", value, flags=re.I)
    value = re.sub(r"\bP\.M\.", "PM", value, flags=re.I)
    return pd.to_datetime(value, format="mixed", errors="coerce")

def process(df):
    df["unit_price"] = df["unit_price"].map(convert_price)
    df["paid_price"] = df["quantity"] * df["unit_price"]
    df["timestamp"] = df["timestamp"].map(convert_datetime)
    df["date"] = df["timestamp"].dt.date
