def get_unique_users_count(users_df):
    return users_df["customer_id"].nunique()
