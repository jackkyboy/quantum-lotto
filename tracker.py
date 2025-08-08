# src/analysis/tracker.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def track_psi_over_time(
    df,
    target_digit="all",
    window_size=50,
    alpha=0.4,
    beta=0.3,
    gamma=0.3,
    entangled_pairs=[('6','8'), ('3','7')],
    plot=True
):
    """
    ติดตามค่า Ψ(n) ของเลข 2 หลักย้อนหลังแบบ moving window
    """
    df = df.sort_values("date").copy()
    df["2digits"] = df["3digits"].astype(str).str.zfill(3).str[-2:]
    full_space = [f"{i:02d}" for i in range(100)]

    psi_list, dates, actuals = [], [], []

    for i in range(window_size, len(df)):
        past_digits = df.iloc[i-window_size:i]["2digits"].tolist()
        actual_digit = df.iloc[i]["2digits"]

        freq = pd.Series(past_digits).value_counts(normalize=True)
        B = np.array([freq.get(n, 0) for n in full_space])

        E = np.zeros(100)
        for j, n in enumerate(full_space):
            d1, d2 = n[0], n[1]
            count = sum([(d1, d2) == p or (d2, d1) == p for p in entangled_pairs])
            E[j] = count / len(entangled_pairs)

        x = np.arange(100)
        W = 0.5 + 0.5 * np.sin(2 * np.pi * x / 25 + np.pi / 4)

        psi = alpha * B + beta * E + gamma * W
        psi /= np.sum(psi)

        if target_digit == "all":
            idx = full_space.index(actual_digit)
        elif target_digit in full_space:
            idx = full_space.index(target_digit)
        else:
            continue

        psi_list.append(psi[idx])
        actuals.append(actual_digit)
        dates.append(df.iloc[i]["date"])

    result = pd.DataFrame({
        "date": dates,
        "actual": actuals,
        "psi": psi_list
    })

    if plot:
        plt.figure(figsize=(14, 4))
        label = f"Ψ({target_digit})" if target_digit != "all" else "Ψ(Winner)"
        sns.lineplot(data=result, x="date", y="psi", label=label)
        plt.title(f"📈 Evolution of {label} over Time")
        plt.xlabel("Date")
        plt.ylabel("Ψ(n)")
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.tight_layout()
        plt.show()

    return result


def track_actual_psi_over_time(
    df,
    alpha=0.4,
    beta=0.3,
    gamma=0.3,
    entangled_pairs=[('6','8'), ('3','7')],
    window_size=50,
    target_digit="all"
):
    """
    ติดตามค่า Ψ(n) ของเลขที่ออกจริงย้อนหลัง
    """
    df = df.sort_values("date")
    df["2digits"] = df["3digits"].astype(str).str.zfill(3).str[-2:]
    full_space = [f"{i:02d}" for i in range(100)]

    psi_list, dates, actuals = [], [], []

    for i in range(window_size, len(df)):
        past = df.iloc[i-window_size:i]["2digits"].tolist()
        actual = df.iloc[i]["2digits"]

        freq = pd.Series(past).value_counts(normalize=True)
        B = np.array([freq.get(n, 0) for n in full_space])

        E = np.zeros(100)
        for j, n in enumerate(full_space):
            d1, d2 = n[0], n[1]
            count = sum([(d1, d2) == p or (d2, d1) == p for p in entangled_pairs])
            E[j] = count / len(entangled_pairs)

        x = np.arange(100)
        W = 0.5 + 0.5 * np.sin(2 * np.pi * x / 25 + np.pi / 4)

        psi = alpha * B + beta * E + gamma * W
        psi /= np.sum(psi)

        if target_digit == "all":
            idx = full_space.index(actual)
        elif target_digit in full_space:
            idx = full_space.index(target_digit)
        else:
            continue

        psi_list.append(psi[idx])
        actuals.append(actual)
        dates.append(df.iloc[i]["date"])

    df_result = pd.DataFrame({
        "date": dates,
        "actual": actuals,
        "psi": psi_list
    })

    # แสดงกราฟทันที
    plt.figure(figsize=(14, 4))
    label = f"Ψ({target_digit})" if target_digit != "all" else "Ψ(Actual)"
    sns.lineplot(x=dates, y=psi_list, label=label)
    plt.title(f"📈 Ψ(n) ของเลขที่ออกย้อนหลัง")
    plt.xlabel("Date")
    plt.ylabel("Ψ(n)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()

    return df_result
