import pandas as pd
import streamlit as st
from outliers import smirnov_grubbs as grubbs
from src.dashboard.anomalies.anomalies import get_param, show_list_of_anomalies

def calculate_grubbs_anomalies(series, alpha):
    indices = grubbs.two_sided_test_indices(series, alpha=alpha)
    return pd.DataFrame({"value": series.iloc[indices]})

def show_grubbs_anomalies(series, mine_name):
    st.subheader("Anomalies detected by Grubbs test:")
    alpha = get_param("alpha:", min_value=0.01, max_value=1.0, value=0.05, step=0.01,key=f"grubbs_alpha_{mine_name}")
    anomalies = calculate_grubbs_anomalies(series, alpha)
    show_list_of_anomalies(anomalies)
