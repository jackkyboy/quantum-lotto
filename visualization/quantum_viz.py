# 📁 /Users/apichet/quantum_lotto/src/visualization/quantum_viz.py

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

def collapse_from_quantum_field(df_qfield, n=5, seed=2025):
    """
    จำลองการ collapse ของคลื่นความน่าจะเป็น → สุ่มเลข n ตัวจาก quantum field ตามน้ำหนัก
    """
    if seed is not None:
        np.random.seed(seed)

    if "number" not in df_qfield or "likelihood" not in df_qfield:
        raise ValueError("❌ DataFrame ต้องมีคอลัมน์ 'number' และ 'likelihood'")

    df_qfield = df_qfield.sort_values("likelihood", ascending=False).copy()
    df_qfield["likelihood"] /= df_qfield["likelihood"].sum()

    choices = df_qfield["number"].values
    probs = df_qfield["likelihood"].values

    collapsed = list(np.random.choice(choices, size=n, replace=False, p=probs))
    print(f"\n🎯 Collapsed Numbers (n={n}): {collapsed}")
    return collapsed


def visualize_quantum_field_and_superposition(df_qfield, top_n=50):
    """
    แสดง Quantum Likelihood Field และ Superposition Matrix
    """
    if "number" not in df_qfield or "likelihood" not in df_qfield:
        raise ValueError("❌ DataFrame ต้องมีคอลัมน์ 'number' และ 'likelihood'")

    df_qfield = df_qfield.sort_values("likelihood", ascending=False).head(top_n).copy()
    df_qfield["likelihood"] /= df_qfield["likelihood"].sum()

    # 🌌 Quantum Likelihood Field
    plt.figure(figsize=(14, 6))
    sns.barplot(data=df_qfield, x="number", y="likelihood")
    plt.xticks(rotation=90)
    plt.title(f"🌌 Quantum Likelihood Field (Top {top_n})")
    plt.xlabel("3-Digit Number")
    plt.ylabel("Normalized Likelihood")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

    # 🧠 Superposition Matrix
    matrix_size = int(np.ceil(np.sqrt(top_n)))
    padded_size = matrix_size ** 2
    padded_data = df_qfield["likelihood"].tolist() + [0.0] * (padded_size - len(df_qfield))

    matrix = np.array(padded_data).reshape((matrix_size, matrix_size))

    plt.figure(figsize=(6, 6))
    sns.heatmap(matrix, cmap="viridis", annot=False, square=True, cbar=True)
    plt.title("🧠 Schrödinger Superposition Matrix")
    plt.tight_layout()
    plt.show()

    print("✅ Visualization สำเร็จ: Quantum Field + Superposition Matrix")


def visualize_digit_entanglement(df_qfield, top_n=100):
    """
    แสดง Heatmap การพัวพันของตัวเลขแต่ละหลัก (หลักร้อย สิบ หน่วย)
    """
    df = df_qfield.sort_values("likelihood", ascending=False).head(top_n).copy()
    digits = df["number"].astype(str).str.zfill(3)
    df["d1"] = digits.str[0]
    df["d2"] = digits.str[1]
    df["d3"] = digits.str[2]

    pairs = []
    for _, row in df.iterrows():
        pairs.extend([
            (row["d1"], row["d2"]),
            (row["d2"], row["d3"]),
            (row["d1"], row["d3"])
        ])

    pair_counts = Counter(pairs)

    matrix = np.zeros((10, 10))
    for (a, b), count in pair_counts.items():
        matrix[int(a), int(b)] += count

    plt.figure(figsize=(7, 6))
    sns.heatmap(matrix, annot=True, fmt=".0f", cmap="magma", cbar=True, square=True)
    plt.title("🧬 Entangled Digit Pair Frequency")
    plt.xlabel("Digit B")
    plt.ylabel("Digit A")
    plt.tight_layout()
    plt.show()

    print("✅ Entangled Digit Heatmap สำเร็จ")


def extract_top_2digit_from_qfield(df_qfield, top_n=10, verbose=True, plot=True):
    """
    วิเคราะห์และเลือกเลข 2 ตัวท้ายจาก Quantum Likelihood Field
    """
    df = df_qfield.copy()
    df["2digit"] = df["number"].astype(str).str[-2:]

    two_digit_summary = (
        df.groupby("2digit")["likelihood"]
        .sum()
        .reset_index()
        .sort_values("likelihood", ascending=False)
        .head(top_n)
    )

    if verbose:
        print(f"\n🔝 Top {top_n} Two-Digit Numbers by Likelihood:")
        for _, row in two_digit_summary.iterrows():
            print(f"🎯 {row['2digit']} → {row['likelihood']:.4%}")

    if plot:
        plt.figure(figsize=(10, 5))
        sns.barplot(data=two_digit_summary, x="2digit", y="likelihood")
        plt.title(f"Top {top_n} Two-Digit Numbers from Quantum Field")
        plt.xlabel("2-Digit Number")
        plt.ylabel("Aggregated Likelihood")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    return two_digit_summary
