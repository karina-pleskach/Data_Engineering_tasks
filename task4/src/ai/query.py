import pandas as pd

def select_columns(df, columns):
    if columns:
        return df[columns]
    return df

def limit_data(df, limit):
    if limit is None:
        return df
    return df.head(limit)

def sort_data(df, sorting):
    for item in sorting[::-1]:
        df = df.sort_values(
            by=item["column"],
            ascending=item.get("ascending", True),
            na_position="last"
        )
    return df

def remove_duplicates(df, distinct):
    if distinct is True:
        return df.drop_duplicates()
    if isinstance(distinct, list):
        return df.drop_duplicates(subset=distinct)
    return df

def group_and_aggregate(df, group_by, aggregations):
    if not aggregations:
        return df
    if group_by is None:
        return aggregate_without_groups(df, aggregations)
    return aggregate_by_groups(df, group_by, aggregations)

def aggregate_without_groups(df, aggregations):
    result = {}
    for agg in aggregations:
        result[agg["as"]] = getattr(df[agg["column"]], agg["function"])()
    return pd.DataFrame([result])

def aggregate_by_groups(df, group_by, aggregations):
    if isinstance(group_by, str):
        group_by = [group_by]
    named_aggs = {agg["as"] : (agg["column"], agg["function"]) for agg in aggregations}
    return df.groupby(group_by, dropna=False).agg(**named_aggs).reset_index()

def filter_data(df, condition):
    if not condition:
        return df
    filter_mask = get_filter_mask(df, condition)
    return df.loc[filter_mask]

def get_filter_mask(df, condition):
    if "conditions" in condition:
        logic = condition["logic"]
        masks = [get_filter_mask(df, item) if "conditions" in item else generate_mask(df, item) for item in condition["conditions"]]
        mask = masks[0]
        if logic == "and":
            for item in masks[1:]:
                mask &= item
        elif logic == "or":
            for item in masks[1:]:
                mask |= item
        return mask
    return generate_mask(df, condition)

def generate_mask(df, condition):
    column = condition["column"]
    operator = condition["operator"]
    value = condition.get("value")
    series = df[column]
    if operator == "is_null":
        return series.isna()
    if operator == "is_not_null":
        return series.notna()
    if operator == "eq":
        return series.eq(value)
    if operator == "ne":
        return series.ne(value)
    if operator == "gt":
        return series.gt(value)
    if operator == "lt":
        return series.lt(value)
    if operator == "gte":
        return series.ge(value)
    if operator == "lte":
        return series.le(value)
    if operator == "in":
        return series.isin(value)
    if operator == "contains":
        return series.astype("string").str.contains(str(value), case=False, regex=False, na=False)
    if operator == "starts_with":
        return series.astype("string").str.startswith(str(value), na=False)
    if operator == "ends_with":
        return series.astype("string").str.endswith(str(value), na=False)
    if operator == "regex":
        return series.astype("string").str.fullmatch(str(value), na=False)

def merge_tables(df, data, joins):
    for join in joins:
        table_name = join["table"]
        df = df.merge(
            data[join["table"]],
            left_on=join["left_on"],
            right_on=join["right_on"],
            how=join.get("how", "inner"),
            suffixes=("", f"_{table_name}")
        )
    return df

def query(data, specification):
    df = data[specification["from"]].copy()
    df = merge_tables(df, data, specification.get("joins", []))
    df = filter_data(df, specification.get("where"))
    df = group_and_aggregate(df, specification.get("group_by"), specification.get("aggregations", []))
    df = filter_data(df, specification.get("having"))
    df = remove_duplicates(df, specification.get("distinct"))
    df = sort_data(df, specification.get("sort", []))
    df = limit_data(df, specification.get("limit"))
    df = select_columns(df, specification.get("columns"))
    return df
