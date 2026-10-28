import streamlit as st
import src.dashboard.analysis as analysis
from src.dashboard.charts import show_charts
from src.dashboard.report import generate_report

def get_all_tabs(df):
    return ["All mines"] + df.columns.tolist()

def union_columns(df):
    return df.sum(axis=1).rename("Total output")

def show_tab(df, tab_name):
    if tab_name == "All mines":
        series = union_columns(df)
    else:
        series = df[tab_name]
    analysis.show_statistics(series, tab_name)

def show_all(df):
    st.download_button("Download PDF report", generate_report(df), "mining_report.pdf", "application/pdf")
    mines = get_all_tabs(df)
    tabs = st.tabs(mines + ["Data", "Charts"])
    for mine, tab in zip(mines, tabs):
        with tab:
            show_tab(df, mine)
    with tabs[-2]:
        st.dataframe(df)
    with tabs[-1]:
        show_charts(df)
