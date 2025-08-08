import matplotlib.pyplot as plt

def plot_amplitude_hist(amplitudes, title="📈 Reshaped Quantum Amplitudes"):
    plt.figure(figsize=(8, 4))
    plt.hist(amplitudes, bins=40, color="#FF66CC", edgecolor="black", alpha=0.85)
    plt.title(title, fontsize=14)
    plt.xlabel("Amplitude")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()
