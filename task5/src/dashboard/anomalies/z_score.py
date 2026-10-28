import pandas as pd
import streamlit as st
from src.dashboard.anomalies.anomalies import get_param, show_list_of_anomalies

def calculate_z_score_anomalies(series, stats, param):
    z_scores = (series - stats["mean daily output"]) / stats["standard deviation"]
    anomalies = z_scores[z_scores.abs() > param]
    return pd.DataFrame({
        "value": series.loc[anomalies.index],
        "z-score": anomalies
    })

def show_z_score_anomalies(series, mine_name, stats):
    st.subheader("Anomalies detected by z-score:")
    param = get_param("parameter:", min_value=0.1, value=3.0, step=0.1, key=f"z_score_param_{mine_name}")
    anomalies = calculate_z_score_anomalies(series, stats, param)
    show_list_of_anomalies(anomalies)
