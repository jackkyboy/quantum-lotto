import numpy as np
from collections import Counter

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
