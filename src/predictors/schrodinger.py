# /Users/apichet/quantum_lotto/src/predictors/schrodinger.py

# /Users/apichet/quantum_lotto/src/predictors/schrodinger.py
# /Users/apichet/quantum_lotto/src/predictors/schrodinger.py

import numpy as np
from collections import Counter

# หมายเหตุ: ไม่ต้อง import generate_seed_from_date, lock_seed ที่นี่แล้ว
# เราจะรับ seed/np_rng จากฝั่ง caller แทน

def _ensure_rng(seed=None, np_rng=None):
    """
    คืนค่า NumPy Generator (local RNG)
    - ถ้ามี np_rng แล้ว ใช้อันนั้น
    - ถ้าไม่มี np_rng แต่มี seed -> สร้าง Generator ใหม่จาก seed
    - ถ้าไม่มีทั้งคู่ -> raise
    """
    if np_rng is not None:
        return np_rng
    if seed is not None:
        return np.random.default_rng(seed)
    raise ValueError("ต้องส่ง seed หรือ np_rng เพื่อให้ผลเป็น deterministic")

def stochastic_optimal_prediction(
    past_data,
    k=5,
    projection="top_freq",
    seed=None,
    np_rng=None,
):
    """
    สร้างเลขคาดการณ์โดยอิงจากความถี่ (แบบ stochastic optimal)
    ใช้ local RNG แทนการล็อก global
    """
    rng = _ensure_rng(seed=seed, np_rng=np_rng)

    count = Counter(past_data)
    total = sum(count.values())
    if total == 0:
        return []

    probs = {n: v / total for n, v in count.items()}

    if projection == "top_freq":
        resolved = sorted(probs.items(), key=lambda x: -x[1])[:100]
    elif projection == "entangled":
        resolved = [(n, p) for n, p in probs.items() if any(d in n for d in ['3', '6', '8'])]
    else:
        resolved = list(probs.items())

    if not resolved:
        return []

    resolved_keys = [x[0] for x in resolved]
    resolved_probs = np.array([x[1] for x in resolved], dtype=float)

    # normalize กันลอยตัวเลข
    s = resolved_probs.sum()
    if s <= 0:
        return []

    resolved_probs /= s
    k = min(k, len(resolved_keys))

    picks = rng.choice(resolved_keys, size=k, replace=False, p=resolved_probs)
    return list(picks)


def generate_schrodinger_superposition(
    k=5,
    seed=None,
    np_rng=None,
):
    """
    สุ่มตัวเลข 3 หลักด้วยการสร้าง superposition แบบ Schrödinger
    โดยใส่ bias ให้กับตัวเลขที่มี entangled digit ('3', '6', '8')

    ใช้ local RNG (np.random.Generator) เพื่อหลีกเลี่ยงผลข้างเคียงแบบ global
    """
    rng = _ensure_rng(seed=seed, np_rng=np_rng)

    full_space = [f"{i:03d}" for i in range(1000)]

    # สุ่ม amplitude แบบฐาน
    base_amplitudes = rng.random(1000)  # ~ U(0,1)

    # ใส่ bias ตามจำนวน entangled digits
    entangled_digits = ['3', '6', '8']
    for idx, val in enumerate(full_space):
        entangled_count = sum(d in val for d in entangled_digits)
        base_amplitudes[idx] *= (1 + 0.25 * entangled_count)

    # ทำเป็น distribution
    denom = base_amplitudes.sum()
    if denom <= 0:
        # fallback (แทบจะไม่เกิด แต่กันไว้)
        wave_probs = np.full(1000, 1/1000)
    else:
        wave_probs = base_amplitudes / denom

    samples = rng.choice(full_space, size=k, replace=True, p=wave_probs)
    return list(samples)
