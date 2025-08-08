from collections import Counter

def get_monthly_top_3digits(df):
    df["month"] = df["date"].dt.month
    df["3digits"] = df["3digits"].astype(str)
    return df.groupby("month")["3digits"].apply(lambda x: Counter(x.dropna()).most_common(1)[0][0])

def get_top_tail2(df, top_k=10):
    df["2digits"] = df["3digits"].astype(str).str[-2:]
    tail2_counter = Counter(df["2digits"])
    return tail2_counter.most_common(top_k)
