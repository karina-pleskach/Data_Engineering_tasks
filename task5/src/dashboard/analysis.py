import pandas as pd
import streamlit as st
from src.dashboard.anomalies.iqr import show_iqr_anomalies
from src.dashboard.anomalies.z_score import show_z_score_anomalies
from src.dashboard.anomalies.moving_average import show_moving_average_anomalies
from src.dashboard.anomalies.grubbs import show_grubbs_anomalies

def calculate_general_statistics(series):
    return series.agg({
        "mean daily output": "mean",
        "standard deviation": "std",
        "median": "median",
        "interquartile range": lambda s: s.quantile(0.75) - s.quantile(0.25),
        "q1": lambda s: s.quantile(0.25),
        "q3": lambda s: s.quantile(0.75)
    })

def show_generaL_statistics(stats):
    with st.container(border=True):
        st.subheader("Statistics:")
        for col, name in zip(st.columns(4), ["mean daily output", "standard deviation", "median", "interquartile range"]):
            col.metric(name, round(stats[name], 2))

def show_anomalies(series, mine_name, stats):
    with st.container(border=True):
        show_iqr_anomalies(series, mine_name, stats)
        show_z_score_anomalies(series, mine_name, stats)
        show_moving_average_anomalies(series, mine_name)
        show_grubbs_anomalies(series, mine_name)

def show_statistics(series, mine_name):
    stats = calculate_general_statistics(series)
    show_generaL_statistics(stats)
    show_anomalies(series, mine_name, stats)
