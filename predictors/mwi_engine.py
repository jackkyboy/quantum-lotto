import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

def mwi_sample_amplitudes(probs, full_space, k=5, n_worlds=10000, seed=None):
    np.random.seed(seed)
    samples = []
    for _ in range(n_worlds):
        picks = np.random.choice(full_space, size=k, replace=False, p=probs)
        samples.extend(picks)
    return Counter(samples)

def show_top_from_mwi(counts, top_n=10):
    top_data = counts.most_common(top_n)
    df_top = pd.DataFrame(top_data, columns=["Number", "Frequency"])

    plt.figure(figsize=(10, 5))
    plt.bar(df_top["Number"], df_top["Frequency"], color="skyblue", edgecolor="black")
    plt.title(f"🌌 Top {top_n} Picks from MWI-Inspired Collapse")
    plt.xlabel("3-Digit Number")
    plt.ylabel("Frequency in Many Worlds")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

    return df_top

def highlight_high_certainty_from_mwi(counter, top_n=10):
    from numpy import log2
    total = sum(counter.values())
    probs = {k: v / total for k, v in counter.items()}
    entropy = -sum(p * log2(p) for p in probs.values() if p > 0)

    print(f"\n📊 Entropy from MWI Simulation: {entropy:.4f} bits")
    print(f"✅ High Certainty Picks (Top {top_n}):")
    for num, prob in sorted(probs.items(), key=lambda x: -x[1])[:top_n]:
        print(f"🎯 {num} → {prob:.4%}")

    return [num for num, _ in sorted(probs.items(), key=lambda x: -x[1])[:top_n]]
