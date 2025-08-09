import numpy as np

def quantum_weighted_sample(wave, k=5, seed=None):
    if seed is not None:
        np.random.seed(seed)
    nums = list(wave.keys())
    probs = np.array(list(wave.values()))
    if probs.sum() == 0 or len(nums) == 0:
        return []
    probs = probs / probs.sum()
    k = min(k, len(nums))
    return np.random.choice(nums, size=k, replace=False, p=probs)
