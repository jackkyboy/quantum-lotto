from collections import Counter
import numpy as np

def find_abused_digits(series, top_n=3, verbose=True):
    digit_counts = Counter()
    for val in series:
        digit_counts.update(val)

    most_common = digit_counts.most_common(top_n)
    
    if verbose:
        print("\n🔥 Top Overused Digits:")
        for d, c in most_common:
            print(f"➤ Digit '{d}' → {c} times")
    
    return most_common


def frequency_drift_over_time(df, chunk_size=5, show_summary=True):
    if "3digits" not in df.columns:
        raise ValueError("DataFrame must contain a '3digits' column.")
    
    chunks = [df.iloc[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
    avg_freqs = [np.mean(list(Counter(chunk["3digits"]).values())) for chunk in chunks]

    if show_summary:
        drift_summary = np.round(avg_freqs, 2)
        print(f"\n📈 ค่าเฉลี่ยความถี่แต่ละช่วงเวลา ({len(drift_summary)} ช่วง):")
        print(drift_summary if len(drift_summary) <= 20 else f"{drift_summary[:10]} ...")

    return avg_freqs
