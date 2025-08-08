import numpy as np

def generate_boosted_quantum_picks(entangled_pairs, boost_factor=0.5, k=5, seed=None):
    if seed is not None:
        np.random.seed(seed)

    full_space = [f"{i:03d}" for i in range(1000)]
    boost_digits = set()
    for pair, _ in entangled_pairs:
        boost_digits.update(pair)

    amplitudes = []
    for val in full_space:
        boost = sum(d in val for d in boost_digits)
        amplitude = 1 + boost_factor * boost
        amplitudes.append(amplitude)

    probs = np.array(amplitudes) / sum(amplitudes)
    picks = np.random.choice(full_space, size=k, replace=False, p=probs)

    print("\n🎯 Pair-Boosted Quantum Picks:")
    for p in picks:
        print("⚡️", p)
    return picks
