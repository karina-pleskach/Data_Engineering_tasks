import streamlit as st
from src.data.load.google_sheets import load_data
from src.data.process.data_processor import process_data
import src.dashboard.view as view
from config import GOOGLE_SHEETS_URL

# @st.cache_data
def load_mines_data(url):
    return process_data(load_data(url))

def configure_dashboard():
    st.set_page_config(page_title="Task5")
    st.title("Mining ops simulator")

def run_dashboard():
    configure_dashboard()
    df = load_mines_data(GOOGLE_SHEETS_URL)
    view.show_all(df)
