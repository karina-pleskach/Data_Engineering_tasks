from src.data.load.google_sheets import load_data
from src.data.process.data_processor import process_data
from config import GOOGLE_SHEETS_URL
import pandas as pd
from outliers import smirnov_grubbs as grubbs

df = process_data(load_data(GOOGLE_SHEETS_URL))

print(df)

print(grubbs.two_sided_test_indices(df['LV-426'], alpha=1.0))
