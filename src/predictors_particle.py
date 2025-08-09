# src/predictors_particle.py

import numpy as np
import pandas as pd
from collections import Counter


def extract_tail2_digits(df):
    """ดึงเลขท้าย 2 ตัวจาก '3digits'."""
    return df["3digits"].astype(str).str.zfill(3).str[-2:].tolist()


def predict_2digit_particle_field(
    past_2digits,
    k=5,
    alpha=0.4,
    beta=0.3,
    gamma=0.3,
    entangled_pairs=None,
    seed=None,
    np_rng=None,
):
    """
    ทำนายเลขท้าย 2 ตัวโดยใช้ Particle Field Model (local RNG)

    Parameters
    ----------
    past_2digits : list of str
        ข้อมูลผลย้อนหลังเลขท้าย 2 ตัว
    k : int
        จำนวนเลขที่จะทำนาย
    alpha, beta, gamma : float
        ค่าถ่วงน้ำหนักสำหรับ bias, entangled effect, wave function
    entangled_pairs : list of tuple
        คู่ตัวเลขที่ถือว่ามี entanglement
    seed : int
        ค่า seed (ใช้ถ้าไม่ได้ส่ง np_rng)
    np_rng : np.random.Generator
        Local RNG สำหรับการสุ่ม
    """
    if entangled_pairs is None:
        entangled_pairs = [('6', '8'), ('3', '7')]

    # ✅ ใช้ local RNG
    if np_rng is None:
        if seed is None:
            raise ValueError("ต้องส่ง seed หรือ np_rng")
        np_rng = np.random.default_rng(seed)

    # เตรียม sample space 00–99
    full_space = [f"{i:02d}" for i in range(100)]

    # Bias จากความถี่ในอดีต
    freq = pd.Series(past_2digits).value_counts(normalize=True)
    B = np.array([freq.get(n, 0) for n in full_space])

    # ผลจาก entanglement
    E = np.zeros(100)
    for i, n in enumerate(full_space):
        d1, d2 = n[0], n[1]
        count = sum([(d1, d2) == p or (d2, d1) == p for p in entangled_pairs])
        E[i] = count / len(entangled_pairs)

    # คลื่น wave function
    x = np.arange(100)
    W = 0.5 + 0.5 * np.sin(2 * np.pi * x / 25 + np.pi / 4)

    # คำนวณ psi
    psi = alpha * B + beta * E + gamma * W
    psi /= np.sum(psi)

    # สุ่ม picks ด้วยความน่าจะเป็น psi (ใช้ local RNG)
    size = min(k, len(full_space))
    picks = np_rng.choice(full_space, size=size, replace=False, p=psi)

    # คืน DataFrame
    result_df = pd.DataFrame({
        "number": full_space,
        "bias": B,
        "entangled": E,
        "wave": W,
        "Ψ(n)": psi
    }).sort_values(by="Ψ(n)", ascending=False).reset_index(drop=True)

    return result_df, list(picks)


def run_simulation_over_n_draws(df, n_draws=100, k=5, seed=None, np_rng=None):
    """
    รันการจำลองการทำนายย้อนหลังเพื่อวัด accuracy.
    """
    if np_rng is None:
        if seed is None:
            raise ValueError("ต้องส่ง seed หรือ np_rng")
        np_rng = np.random.default_rng(seed)

    results = []
    for i in range(n_draws):
        partial_df = df.iloc[:-(i+1)]
        if len(partial_df) < 10:
            break
        past = extract_tail2_digits(partial_df)
        actual = df.iloc[-(i+1)]["3digits"][-2:]
        _, picks = predict_2digit_particle_field(past, k=k, np_rng=np_rng)
        hit = actual in picks
        results.append(hit)

    accuracy = np.mean(results)
    print(f"\n📊 Accuracy over last {len(results)} draws: {accuracy:.2%}")
    return results


def most_common_entangled_pairs(past_2digits, top_k=5):
    pairs = [(x[0], x[1]) for x in past_2digits if len(x) == 2]
    c = Counter(pairs + [(b, a) for a, b in pairs])
    return c.most_common(top_k)


# ✅ สำหรับ backend API
def run_particle_prediction(df, return_predictions=False, seed=None, np_rng=None):
    """
    Wrapper สำหรับรันทำนาย Particle Field ใน backend
    """
    if np_rng is None:
        if seed is None:
            raise ValueError("ต้องส่ง seed หรือ np_rng")
        np_rng = np.random.default_rng(seed)

    past_2digits = extract_tail2_digits(df)
    entangled = most_common_entangled_pairs(past_2digits, top_k=5)
    result_df, picks = predict_2digit_particle_field(
        past_2digits,
        entangled_pairs=entangled,
        k=5,
        np_rng=np_rng
    )

    if return_predictions:
        return picks

    print("🎯 ทำนายเลขท้าย 2 ตัวจาก Particle Field:")
    for num in picks:
        print(f"🔮 {num}")

    return result_df
