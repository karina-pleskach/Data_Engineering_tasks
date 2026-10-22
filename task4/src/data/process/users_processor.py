def find_root(parent, x):
    if parent[x] != x:
        parent[x] = find_root(parent, parent[x])
    return parent[x]

def union(parent, a, b):
    parent[find_root(parent, a)] = find_root(parent, b)

def are_same_user(a, b):
    fields = ["name", "address", "phone", "email"]
    return sum(a[f] == b[f] for f in fields) >= 3

def assign_customer_ids(users_df):
    rows = users_df.to_dict("records")
    parent = {row["id"]: row["id"] for row in rows}
    for i, a in enumerate(rows):
        for b in rows[i+1:]:
            if are_same_user(a, b):
                union(parent, a["id"], b["id"])
    users_df["customer_id"] = [find_root(parent, x) for x in users_df["id"]]

def process(df):
    assign_customer_ids(df)
    df["phone"] = df["phone"].str.replace(r"\s+|\.+|\(+|\)+|\-+", "", regex=True)
