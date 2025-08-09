import numpy as np

def compute_entropy(counter):
    total = sum(counter.values())
    probs = [v / total for v in counter.values()]
    entropy = -sum(p * np.log2(p) for p in probs if p > 0)
    return entropy

def normalize_freq(counter_obj):
    total = sum(counter_obj.values())
    if total == 0:
        return {}
    return {k: v / total for k, v in counter_obj.items()}
