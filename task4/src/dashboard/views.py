import streamlit as st
from src.analytics.books_analyzer import *
from src.analytics.orders_analyzer import *
from src.analytics.users_analyzer import *
from src.ai.client import ask_ai

def show_top_days(orders_df):
    st.subheader("Top 5 days by revenue:")
    st.dataframe(get_top_revenue_by_date(orders_df))

def show_general_statistics(users_df, books_df):
    st.subheader("General statistics:")
    cols = st.columns(2)
    cols[0].metric("Number of unique users", get_unique_users_count(users_df))
    cols[1].metric("Number of unique sets of authors", get_unique_author_sets_count(books_df))

def show_top_statistics(books_df, orders_df, users_df):
    st.subheader("Top statistics:")
    cols = st.columns([2, 1])
    with cols[0]:
        st.metric("The name of most popular author(s)", "")
        st.write(", ".join(get_top_author_set(books_df, orders_df)))
    with cols[1]:
        st.metric("Best buyer", "")
        st.write(list(get_top_customer_user_ids_by_spending(users_df, get_top_customer_id_by_spending(orders_df))))

def show_revenue_chart(orders_df):
    st.subheader("Daily revenue chart:")
    st.line_chart(get_revenue_by_date(orders_df).astype(float).sort_index())

def show_info_elements(books_df, orders_df, users_df):
    show_top_days(orders_df) 
    show_general_statistics(users_df, books_df)
    show_top_statistics(books_df, orders_df, users_df)
    show_revenue_chart(orders_df)

def show_ai_question(store_num, data):
    st.subheader("Ask me about this store:")
    with st.form(key=f"question_form_{store_num}"):
        question = st.text_input("Your question...")
        submitted = st.form_submit_button("Ask")
    if submitted:
        with st.container(border=True):
            st.write(ask_ai(question, data))

def show_store_view(data, store_num):
    books_df = data["books"]
    users_df = data["users"]
    orders_df = data["orders"]
    show_ai_question(store_num, data)
    show_info_elements(books_df, orders_df, users_df)
