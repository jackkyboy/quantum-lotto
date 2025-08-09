import numpy as np

def unitary_cat_collapse_two_digit(k=5, delta_phase=0.3, collapse_threshold=0.6, seed=None):
    """
    🐱 Simulate Unitary Collapse of Schrödinger Cat in 2-digit system
    Inspired by parity-breaking collapse
    """
    if seed is not None:
        np.random.seed(seed)

    full_space = [f"{i:02d}" for i in range(100)]
    base_amplitudes = np.ones(100) / 100

    left_phases = np.random.normal(0, delta_phase, 100)
    right_phases = np.random.normal(0, delta_phase, 100)
    asymmetry = np.abs(left_phases - right_phases)

    collapse_mask = asymmetry > collapse_threshold
    collapsed_amplitudes = np.where(collapse_mask, base_amplitudes, 0)
    norm = collapsed_amplitudes.sum()

    if norm == 0:
        collapsed_amplitudes = base_amplitudes
        norm = 1

    probs = collapsed_amplitudes / norm
    return np.random.choice(full_space, size=k, replace=False, p=probs)
