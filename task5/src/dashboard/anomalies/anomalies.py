import pandas as pd
import streamlit as st

def get_param(input, min_value, value, step, key, max_value=None):
    return st.number_input(input, min_value=min_value, max_value=max_value, value=value, step=step, key=key)

def show_list_of_anomalies(anomalies):
    if anomalies.empty:
        st.write("No anomalies found.")
    else:
        st.dataframe(anomalies)
