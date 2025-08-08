import numpy as np

def simulate_collapse_from_8d(df_8d, k=5, method="exp", seed=42):
    np.random.seed(seed)
    base = df_8d["freq"] + df_8d["entangle"] + df_8d["monthly"]

    if method == "exp":
        amp = np.exp(base)
    elif method == "sqrt":
        amp = np.sqrt(base)
    else:
        amp = base

    probs = amp / amp.sum()
    picks = np.random.choice(df_8d["number"], size=k, replace=False, p=probs)

    print(f"\n🎯 Quantum Collapse from 8D Field ({method}):")
    for p in picks:
        print("💫", p)
    return picks
