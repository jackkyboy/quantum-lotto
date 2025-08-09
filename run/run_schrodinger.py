from config import get_seed
# run/run_schrodinger.py
# run/run_schrodinger.py

from predictors.schrodinger import generate_schrodinger_superposition
from predictors.stochastic import stochastic_optimal_prediction
from predictors.unitary_collapse import unitary_cat_collapse_two_digit
from analysis.backtest import backtest_schr_simulation
from utils.statistics import compute_entropy
from config import generate_seed_from_date, lock_seed



import pandas as pd
from collections import Counter


def run_schrodinger_simulation(df):
    import os  # 👈 เพิ่ม import ที่นี่

    sim_results_10k = generate_schrodinger_superposition(k=10000, seed=get_seed())
    sim_counter_10k = Counter(sim_results_10k)

    print("\n🎲 Simulation: Top 10 from 10,000 Schrödinger Rounds:")
    for num, count in sim_counter_10k.most_common(10):
        print(f"🔮 {num} → {count} ครั้ง")

    # ✅ สร้างโฟลเดอร์ outputs หากยังไม่มี
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))
    os.makedirs(output_dir, exist_ok=True)

    # ✅ Save CSV ลง outputs
    output_file = os.path.join(output_dir, "quantum_sim_10000.csv")
    pd.DataFrame(sim_results_10k, columns=["prediction"]).to_csv(output_file, index=False)

    actual_set = set(df["3digits"].tolist())
    hits = sum(1 for val in sim_results_10k if val in actual_set)
    print(f"\n✅ Hits: {hits} / 10000")

    entropy_val = compute_entropy(sim_counter_10k)
    print(f"📊 Entropy: {entropy_val:.4f} bits")

    print("\n🧠 Stochastic Optimal Prediction (KS-Inspired):")
    for num in stochastic_optimal_prediction(df["3digits"].astype(str).tolist(), k=5):
        print("🔮", num)

    combined_preds = set([x[0] for x in sim_counter_10k.most_common(5)])
    combined_preds.update(stochastic_optimal_prediction(df["3digits"].astype(str).tolist(), k=5))
    print("\n📦 Combined Quantum Picks:")
    for num in sorted(combined_preds):
        print("🔗", num)

    return sim_results_10k, sim_counter_10k, hits



def run_unitary_collapse():
    print("\n🐱 Schrödinger Collapse via Parity Breaking (Unitary):")
    unitary_results = unitary_cat_collapse_two_digit(k=5, seed=2025)
    for n in unitary_results:
        print("🔻", n)


def run_backtest(df):
    past_results = df["3digits"].tolist()
    hits, top10_simulated = backtest_schr_simulation(past_results)
    print(f"\n🔍 พบผลจริง {len(hits)} รายการใน Schrödinger Simulation")
    return hits, top10_simulated


# ✅ CLI: เรียกตรง
if __name__ == "__main__":
    import sys
    import os
    import json
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    # 👉 โหลดจาก JSON (resolve absolute path)
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "lotto_110year_full_fixed.json")
    json_path = os.path.abspath(json_path)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # 🔁 เตรียมคอลัมน์ "3digits"
    digit_cols = ["front3_1", "front3_2", "last3_1", "last3_2", "last3_3"]
    available_cols = [col for col in digit_cols if col in df.columns]
    df["3digits"] = df[available_cols].astype(str).values.tolist()

    df_exploded = pd.DataFrame(df["3digits"].tolist(), index=df.index).melt()["value"]
    df_full = pd.DataFrame({"3digits": df_exploded.dropna().astype(str)})

    # 🎯 รัน Simulation + Backtest
    sim_results, sim_counter, hits = run_schrodinger_simulation(df_full)
    run_unitary_collapse()
    backtest_hits, top10_simulated = run_backtest(df_full)

    print(f"\n✅ Schrödinger Simulation สำเร็จทั้งหมด! 🎉")
    print(f"🔁 จำนวนรอบซิมูเลชัน: {len(sim_results)}")
    print(f"🎯 จำนวนที่ตรงกับผลจริง (ในซิมูเลชันล่าสุด): {hits}")
    print(f"🧪 จำนวนที่ตรงจาก backtest: {len(backtest_hits)}")
