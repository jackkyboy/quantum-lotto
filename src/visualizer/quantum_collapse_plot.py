import matplotlib.pyplot as plt
import numpy as np

def plot_schrodinger_lotto(predictions, title="🎲 Schrödinger Quantum Picks Collapse"):
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(predictions, np.ones(len(predictions)), width=0.5)

    ax.set_facecolor("#0A0A0A")
    fig.patch.set_facecolor("#0A0A0A")
    for bar in bars:
        bar.set_color("#00FF99")
        bar.set_edgecolor("#39FF14")
        bar.set_linewidth(1.2)

    ax.set_title(title, fontsize=18, color="#00FF99", pad=20)
    ax.set_ylabel("Probability Collapse", fontsize=12, color="#AAAAAA")
    ax.set_yticks([])
    ax.tick_params(axis='x', colors='white', labelsize=14)
    ax.spines['bottom'].set_color('#39FF14')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    for idx, val in enumerate(predictions):
        ax.text(idx, 1.05, f"{val}", ha='center', va='bottom', fontsize=16, color="#00FFFF")

    plt.tight_layout()
    plt.show()


def plot_amplitude_hist(amplitudes, title="📈 Reshaped Quantum Amplitudes"):
    plt.figure(figsize=(8, 4))
    plt.hist(amplitudes, bins=40, color="#FF66CC", edgecolor="black", alpha=0.85)
    plt.title(title, fontsize=14)
    plt.xlabel("Amplitude")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()
