def add_date_features(df):
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["weekday"] = df["date"].dt.weekday
    return df

def add_digit_features(df):
    digits = df["3digits"].astype(str).str.zfill(3)
    for i in range(3):
        df[f"d{i+1}"] = digits.str[i].astype(int)
    df["sum_digits"] = df[["d1", "d2", "d3"]].sum(axis=1)
    df["has_double"] = (
        (digits.str[0] == digits.str[1]) |
        (digits.str[1] == digits.str[2]) |
        (digits.str[0] == digits.str[2])
    ).astype(int)
    return df
