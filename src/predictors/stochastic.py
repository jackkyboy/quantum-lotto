import numpy as np
from collections import Counter

def stochastic_optimal_prediction(
    past_data,
    k=5,
    projection="top_freq",
    seed=None,
    np_rng=None,
):
    """
    สร้างเลขคาดการณ์โดยอิงจากความถี่ (stochastic optimal) แบบ deterministic ด้วย local RNG
    - ส่ง np_rng (np.random.Generator) หรือ seed อย่างใดอย่างหนึ่ง
    """
    # ✅ ใช้ local RNG แทน np.random.seed (global)
    if np_rng is None:
        if seed is None:
            raise ValueError("ต้องส่ง seed หรือ np_rng เพื่อให้ deterministic")
        np_rng = np.random.default_rng(seed)

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

    s = resolved_probs.sum()
    if s <= 0:
        return []

    resolved_probs /= s
    k = min(k, len(resolved_keys))
    picks = np_rng.choice(resolved_keys, size=k, replace=False, p=resolved_probs)
    return list(picks)
