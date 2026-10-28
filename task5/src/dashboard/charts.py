import streamlit as st
import numpy as np
import plotly.express as px
from src.dashboard.analysis import calculate_general_statistics
from src.dashboard.anomalies.iqr import calculate_iqr_anomalies

def get_anomalies(series):
    stats = calculate_general_statistics(series)
    return calculate_iqr_anomalies(series, 1.5, stats)

def get_series(df, type):
    if type != "Stacked bar":
        mine_name = st.selectbox("Mine:", df.columns.tolist())
        return df[mine_name]
    return df.sum(axis=1).rename("Total output")

def show_trendline(fig, series, degree):
    x = np.arange(len(series))
    coefficients = np.polyfit(x, series.values, degree)
    trendline = np.polyval(coefficients, x)
    fig.add_scatter(x=series.index, y=trendline, mode="lines", name=f"Trendline (degree {degree})", line=dict(color="green"))

def show_anomalies(fig, anomalies, name="IQR anomalies", color="red"):
    fig.add_scatter(x=anomalies.index, y=anomalies.values, mode="markers", name=name, marker=dict(color=color, size=10))

def show_charts(df):
    chart_type = st.selectbox("Chart type:", ["Line", "Bar", "Stacked bar"])
    degree = st.selectbox("Polynomial degree:", [1, 2, 3, 4], key="polynomial_degree")
    series = get_series(df, chart_type)
    anomalies = get_anomalies(series)
    if chart_type == "Line":
        fig = px.line(series, labels={"index": "Day", "value": "Output"})
    elif chart_type == "Bar":
        colors = ["red" if day in anomalies.index else "blue" for day in series.index]
        fig = px.bar(x=series.index, y=series.values, labels={"x": "Day", "y": "Output"})
        fig.update_traces(marker_color=colors)
    elif chart_type == "Stacked bar":
        fig = px.bar(df, barmode="stack")
    show_trendline(fig, series, degree)
    show_anomalies(fig, anomalies, color="yellow" if chart_type == "Stacked bar" else "red")
    st.plotly_chart(fig, width="stretch")
