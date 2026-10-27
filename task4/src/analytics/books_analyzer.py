def get_unique_author_sets_count(books_df):
    return books_df["author_set"].nunique()

def get_books_sold_count_by_author_set(books_df, orders_df):
    orders = orders_df.merge(books_df[["id", "author_set"]], left_on="book_id", right_on="id")
    return orders.groupby("author_set")["quantity"].sum()

def get_top_author_set(books_df, orders_df):
    return get_books_sold_count_by_author_set(books_df, orders_df).idxmax()