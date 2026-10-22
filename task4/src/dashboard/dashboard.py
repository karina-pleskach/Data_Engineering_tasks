import streamlit as st
from src.data.load.data_loader import load_data
from src.data.process.data_processor import process_data
from src.dashboard.views import show_store_view
from config import STORE_NUMS

@st.cache_data
def load_store_data(store_num):
    return process_data(load_data(store_num))

def show_dashboard():
    st.set_page_config(page_title="Task4")
    st.title("Books stores dashboards")
    tabs = st.tabs([f"Store {i}" for i in STORE_NUMS])
    for store_num, tab in enumerate(tabs, start=1):
        with tab:
            data = load_store_data(store_num)
            show_store_view(data)
