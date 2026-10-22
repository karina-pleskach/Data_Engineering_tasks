import matplotlib.pyplot as plt

def get_revenue_by_date(orders_df):
    return orders_df.groupby("date")["paid_price"].sum()

def get_top_revenue_by_date(orders_df, num=5):
    return get_revenue_by_date(orders_df).sort_values(ascending=False).head(num)

def get_spending_by_customer(orders_df):
    return orders_df.groupby("customer_id")["paid_price"].sum()

def get_top_customer_id_by_spending(orders_df):
    return get_spending_by_customer(orders_df).idxmax()

def get_top_customer_user_ids_by_spending(users_df, customer_id):
    return users_df[users_df["customer_id"] == customer_id]["id"].unique().tolist()

def plot_daily_revenue(orders_df):
    daily_revenue = get_revenue_by_date(orders_df).astype(float)
    daily_revenue.sort_index().plot(kind="line")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.title("Daily revenue:")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("daily_revenue.png")
    plt.close()
