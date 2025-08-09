# run/run_schrodinger.py
# run/run_schrodinger.py
# run/run_schrodinger.py
import os
import hashlib
import pandas as pd
from collections import Counter

from predictors.schrodinger import generate_schrodinger_superposition
from predictors.stochastic import stochastic_optimal_prediction
from predictors.unitary_collapse import unitary_cat_collapse_two_digit
from analysis.backtest import backtest_schr_simulation
from utils.statistics import compute_entropy
from config import make_rngs  # ใช้สร้าง local RNG

# -----------------------------
# Config via ENV
# -----------------------------
DEBUG = os.getenv("DEBUG", "0") == "1"
ENV = os.getenv("ENV", "development")
SCHRO_K = int(os.getenv("SCHRO_K", "10000"))  # จำนวนรอบซิมูฯ ปรับได้

def _hash_series(series: pd.Series) -> str:
    """ทำแฮชข้อมูล (เช่น คอลัมน์ '3digits') เพื่อใช้ cache key"""
    h = hashlib.sha1()
    # ใช้ค่าต่อกันแบบปลอดภัย (หลีกเลี่ยง NaN)
    for v in series.astype(str).tolist():
        h.update(v.encode("utf-8"))
        h.update(b"|")
    return h.hexdigest()

# simple in-memory cache (per-process)
_CACHE = {}

def run_schrodinger_simulation(df, seed=None, np_rng=None, *, k: int | None = None, save_csv: bool = False):
    """
    รัน Schrödinger Simulation (ดีฟอลต์ k=SCHRO_K)
    - ใช้ cache ตาม (seed, data_hash, k) ลดคำนวณซ้ำในโปรดักชัน
    - ปิดการเขียนไฟล์และ print ใน production เพื่อประสิทธิภาพ
    """
    if np_rng is None:
        if seed is None:
            raise ValueError("ต้องส่ง seed หรือ np_rng เพื่อให้ deterministic")
        _, np_rng = make_rngs(seed)

    if "3digits" not in df.columns:
        raise ValueError("df ต้องมีคอลัมน์ '3digits' เป็นสตริงของเลขสามหลัก")

    k = int(k or SCHRO_K)
    data_hash = _hash_series(df["3digits"].dropna().astype(str))
    cache_key = (seed, data_hash, k)

    # ------------------ Cache short-circuit ------------------
    if ENV == "production" and cache_key in _CACHE:
        sim_counter_10k, hits_cached, entropy_val = _CACHE[cache_key]
        return [], sim_counter_10k, hits_cached

    # ------------------ Run simulation ------------------
    sim_results = generate_schrodinger_superposition(k=k, np_rng=np_rng)
    sim_counter = Counter(sim_results)

    if DEBUG:
        print(f"\n🎲 Simulation: Top 10 from {k} Schrödinger Rounds:")
        for num, count in sim_counter.most_common(10):
            print(f"🔮 {num} → {count} ครั้ง")

    # I/O: เขียนไฟล์เฉพาะตอน debug หรือสั่งไว้ชัดเจน
    if save_csv or (DEBUG and ENV != "production"):
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"quantum_sim_{k}.csv")
        pd.DataFrame(sim_results, columns=["prediction"]).to_csv(output_file, index=False)

    # คำนวณ hits/entropy
    actual_set = set(df["3digits"].dropna().astype(str).tolist())
    hits = sum(1 for val in sim_results if val in actual_set)
    entropy_val = compute_entropy(sim_counter)

    if DEBUG:
        print(f"\n✅ Hits: {hits} / {k}")
        print(f"📊 Entropy: {entropy_val:.4f} bits")
        print("\n🧠 Stochastic Optimal Prediction (KS-Inspired):")
        for num in stochastic_optimal_prediction(df['3digits'].astype(str).tolist(), k=5, np_rng=np_rng):
            print("🔮", num)
        combined_preds = set([x[0] for x in sim_counter.most_common(5)])
        combined_preds.update(stochastic_optimal_prediction(df['3digits'].astype(str).tolist(), k=5, np_rng=np_rng))
        print("\n📦 Combined Quantum Picks:")
        for num in sorted(combined_preds):
            print("🔗", num)

    # เก็บ cache เฉพาะ production
    if ENV == "production":
        _CACHE[cache_key] = (sim_counter, hits, entropy_val)

    return sim_results, sim_counter, hits


def run_unitary_collapse(seed=2025):
    _, np_rng = make_rngs(seed)
    if DEBUG:
        print("\n🐱 Schrödinger Collapse via Parity Breaking (Unitary):")
    unitary_results = unitary_cat_collapse_two_digit(k=5, np_rng=np_rng)
    if DEBUG:
        for n in unitary_results:
            print("🔻", n)


def run_backtest(df):
    past_results = df["3digits"].astype(str).tolist()
    hits, top10_simulated = backtest_schr_simulation(past_results)
    if DEBUG:
        print(f"\n🔍 พบผลจริง {len(hits)} รายการใน Schrödinger Simulation")
    return hits, top10_simulated


# CLI คงเดิม (ย้าย I/O ไปตาม DEBUG/save_csv)
if __name__ == "__main__":
    import sys, json
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "lotto_110year_full_fixed.json"))
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    digit_cols = ["front3_1", "front3_2", "last3_1", "last3_2", "last3_3"]
    available_cols = [c for c in digit_cols if c in df.columns]
    df["3digits"] = df[available_cols].astype(str).values.tolist()
    df_exploded = pd.DataFrame(df["3digits"].tolist(), index=df.index).melt()["value"]
    df_full = pd.DataFrame({"3digits": df_exploded.dropna().astype(str)})

    seed = 20250816
    run_schrodinger_simulation(df_full, seed=seed, save_csv=DEBUG)
    run_unitary_collapse(seed=seed)
    run_backtest(df_full)
    print("\n✅ Schrödinger Simulation สำเร็จทั้งหมด! 🎉")
