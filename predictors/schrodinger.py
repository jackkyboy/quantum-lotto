# /Users/apichet/quantum_lotto/src/predictors/schrodinger.py

# /Users/apichet/quantum_lotto/src/predictors/schrodinger.py

import numpy as np
from collections import Counter
from config import generate_seed_from_date, lock_seed


def stochastic_optimal_prediction(past_data, k=5, projection="top_freq", seed=42):
    """
    สร้างเลขคาดการณ์โดยอิงจากความถี่ (แบบ stochastic optimal)
    """
    np.random.seed(seed)
    count = Counter(past_data)
    total = sum(count.values())
    probs = {k: v / total for k, v in count.items()}

    if projection == "top_freq":
        resolved = sorted(probs.items(), key=lambda x: -x[1])[:100]
    elif projection == "entangled":
        resolved = [(n, p) for n, p in probs.items() if any(d in n for d in ['3', '6', '8'])]
    else:
        resolved = list(probs.items())

    resolved_keys = [x[0] for x in resolved]
    resolved_probs = np.array([x[1] for x in resolved])
    if len(resolved_keys) == 0:
        return []

    k = min(k, len(resolved_keys))
    resolved_probs /= resolved_probs.sum()
    return np.random.choice(resolved_keys, size=k, replace=False, p=resolved_probs)


def generate_schrodinger_superposition(k=5, seed=None):
    """
    สุ่มตัวเลข 3 หลักด้วยการสร้าง superposition แบบ Schrödinger
    โดยใส่ bias ให้กับตัวเลขที่มี entangled digit ('3', '6', '8')
    """
    if seed is None:
        raise ValueError("❌ ต้องระบุ seed เข้ามา เช่นจากวันที่ออกรางวัล")

    np.random.seed(seed)

    full_space = [f"{i:03d}" for i in range(1000)]
    base_amplitudes = np.random.rand(1000)

    entangled_digits = ['3', '6', '8']
    for idx, val in enumerate(full_space):
        entangled_count = sum(d in val for d in entangled_digits)
        base_amplitudes[idx] *= (1 + 0.25 * entangled_count)

    wave_probs = base_amplitudes / base_amplitudes.sum()
    samples = np.random.choice(full_space, size=k, replace=True, p=wave_probs)
    return samples
