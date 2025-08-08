import numpy as np

def highlight_high_certainty_quantile(counter, quantile_threshold=0.98, entropy_threshold=None):
    total = sum(counter.values())
    probs = {k: v / total for k, v in counter.items()}
    entropy = -sum(p * np.log2(p) for p in probs.values() if p > 0)

    print(f"\n📊 Entropy: {entropy:.4f} bits")
    if entropy_threshold is not None and entropy > entropy_threshold:
        print("⚠️ Entropy สูงเกินเกณฑ์ ไม่แนะนำให้ใช้งานผลลัพธ์ชุดนี้")
        return []

    sorted_probs = sorted(probs.items(), key=lambda x: -x[1])
    prob_values = [x[1] for x in sorted_probs]
    threshold_value = np.quantile(prob_values, quantile_threshold)

    filtered = [(n, p) for n, p in sorted_probs if p >= threshold_value]
    print(f"\n✅ High Certainty Picks (Quantile ≥ {quantile_threshold}):")
    for n, p in filtered:
        print(f"🎯 {n} → {p:.4%}")

    return [x[0] for x in filtered]


def highlight_high_certainty(counter, top_n=10, entropy_threshold=None):
    import numpy as np
    total = sum(counter.values())
    probs = {k: v / total for k, v in counter.items()}
    entropy = -sum(p * np.log2(p) for p in probs.values() if p > 0)

    print(f"\n📊 Entropy: {entropy:.4f} bits")

    if entropy_threshold is not None and entropy > entropy_threshold:
        print("⚠️ Entropy สูงเกินเกณฑ์ ไม่แนะนำให้ใช้งานผลลัพธ์ชุดนี้")
        return []

    top_items = sorted(probs.items(), key=lambda x: -x[1])[:top_n]
    print(f"\n✅ High Certainty Picks (Top {top_n}):")
    for n, p in top_items:
        print(f"🎯 {n} → {p:.4%}")
    return [x[0] for x in top_items]
