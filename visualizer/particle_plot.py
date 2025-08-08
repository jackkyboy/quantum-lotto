# /Users/apichet/quantum_lotto/src/visualizer/particle_plot.py
import pandas as pd
import numpy as np
from collections import Counter
import os

# ✅ แก้ตรงนี้ให้ใช้ non-GUI backend
import matplotlib
matplotlib.use('Agg')  # 💥 สำคัญมาก!

import matplotlib.pyplot as plt
import seaborn as sns


# ✅ helper: save heatmap of Ψ(n) to file
def plot_particle_field_heatmap(result_df, filename="particle_field_heatmap.png"):
    plt.figure(figsize=(12, 2))
    sns.heatmap(result_df.set_index("number")[["Ψ(n)"]].T, cmap="mako", cbar=True)
    plt.title("🔬 Heatmap of Ψ(n) over 2-digit space")
    plt.xlabel("2-digit number")
    plt.tight_layout()

    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.abspath(os.path.join(output_dir, filename))

    plt.savefig(full_path)
    plt.close()
    print(f"📦 Heatmap saved to: {full_path}")
    return full_path


# 🧬 คู่ Entangled ที่พบบ่อย
def most_common_entangled_pairs(past_2digits, top_k=5):
    pairs = [(x[0], x[1]) for x in past_2digits if len(x) == 2]
    c = Counter(pairs + [(b, a) for a, b in pairs])
    return c.most_common(top_k)


# 📈 Evolution of Ψ(n)
def track_psi_over_time(
    df,
    target_digit="all",
    window_size=50,
    alpha=0.4,
    beta=0.3,
    gamma=0.3,
    entangled_pairs=[('6', '8'), ('3', '7')],
    plot=False,
    save_plot=False,
    filename="psi_evolution.png"
):
    df = df.sort_values("date").copy()
    df["2digits"] = df["3digits"].astype(str).str.zfill(3).str[-2:]
    full_space = [f"{i:02d}" for i in range(100)]

    psi_list, dates, actuals = [], [], []

    for i in range(window_size, len(df)):
        past_digits = df.iloc[i - window_size:i]["2digits"].tolist()
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

        idx = full_space.index(actual_digit) if actual_digit in full_space else None
        if idx is not None:
            psi_list.append(psi[idx])
            actuals.append(actual_digit)
            dates.append(df.iloc[i]["date"])

    result = pd.DataFrame({
        "date": dates,
        "actual": actuals,
        "psi": psi_list
    })

    if save_plot:
        plt.figure(figsize=(14, 4))
        label = f"Ψ({target_digit})" if target_digit != "all" else "Ψ(Winner)"
        sns.lineplot(data=result, x="date", y="psi", label=label)
        plt.title(f"📈 Evolution of {label} over Time")
        plt.xlabel("Date")
        plt.ylabel("Ψ(n)")
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.tight_layout()

        output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, filename)
        plt.savefig(path)
        print(f"📦 Ψ(n) Evolution saved to: {path}")
        plt.close()

    return result


# 📉 ติดตาม Ψ ของเลขที่ถูกรางวัล
def track_actual_psi_over_time(
    df,
    alpha=0.4,
    beta=0.3,
    gamma=0.3,
    entangled_pairs=[('6', '8'), ('3', '7')],
    window_size=50,
    target_digit="all",
    save_plot=False,
    filename="actual_psi_over_time.png"
):
    df = df.sort_values("date")
    df["2digits"] = df["3digits"].astype(str).str.zfill(3).str[-2:]
    full_space = [f"{i:02d}" for i in range(100)]
    psi_list = []
    dates = []
    actuals = []

    for i in range(window_size, len(df)):
        past = df.iloc[i - window_size:i]["2digits"].tolist()
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

        idx = full_space.index(actual) if actual in full_space else None
        if idx is not None:
            psi_list.append(psi[idx])
            actuals.append(actual)
            dates.append(df.iloc[i]["date"])

    result_df = pd.DataFrame({
        "date": dates,
        "actual": actuals,
        "psi": psi_list
    })

    if save_plot:
        plt.figure(figsize=(14, 4))
        label = f"Ψ({target_digit})"
        sns.lineplot(x=dates, y=psi_list, label=label)
        plt.title("📈 Ψ(n) ของเลขที่ถูกรางวัลย้อนหลัง")
        plt.xlabel("Date")
        plt.ylabel("Ψ(n)")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()

        output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, filename)
        plt.savefig(path)
        plt.close()
        print(f"📦 Saved actual ψ(n) chart to: {path}")

    return result_df
