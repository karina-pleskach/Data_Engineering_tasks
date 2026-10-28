import pandas as pd
import streamlit as st
from src.dashboard.anomalies.anomalies import get_param, show_list_of_anomalies

def calculate_moving_average_anomalies(series, window, param):
    moving_average = series.rolling(window=window).mean()
    distance = (series - moving_average) / moving_average * 100
    anomalies = distance[distance.abs() > param]
    return pd.DataFrame({
        "value": series.loc[anomalies.index],
        "distance (percent)": anomalies
    })

def show_moving_average_anomalies(series, mine_name):
    st.subheader("Anomalies detected by distance (percent) from moving average:")
    window, param = (get_param("window (days):", min_value=1, value=7, step=1, key=f"moving_average_window_{mine_name}"), 
                     get_param("parameter:", min_value=0.1, max_value=100.0, value=50.0, step=0.1, key=f"moving_average_param_{mine_name}"))
    anomalies = calculate_moving_average_anomalies(series, window, param)
    show_list_of_anomalies(anomalies)
