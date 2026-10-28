import pandas as pd
import streamlit as st
from src.dashboard.anomalies.anomalies import get_param, show_list_of_anomalies

def calculate_iqr_anomalies(series, param, stats):
    lower_bound = stats["q1"] - param * stats["interquartile range"]
    upper_bound = stats["q3"] + param * stats["interquartile range"]
    return series[(series < lower_bound) | (series > upper_bound)]

def show_iqr_anomalies(series, mine_name, stats):
    st.subheader("Anomalies detected by IQR rule:")
    param = get_param("parameter:", min_value=0.1, value=1.5, step=0.1, key=f"iqr_param_{mine_name}")
    anomalies = calculate_iqr_anomalies(series, param, stats)
    show_list_of_anomalies(anomalies.rename("value"))
