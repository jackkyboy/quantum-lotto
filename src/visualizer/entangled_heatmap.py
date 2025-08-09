import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations

def plot_entangled_heatmap(df):
    matrix = np.zeros((10, 10))
    for val in df["3digits"]:
        digits = set(val)
        for d1, d2 in combinations(digits, 2):
            i, j = sorted((int(d1), int(d2)))
            matrix[i][j] += 1
            matrix[j][i] += 1

    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, annot=True, fmt=".0f", cmap="YlOrRd", xticklabels=range(10), yticklabels=range(10))
    plt.title("🔥 Quantum Entangled Digit Heatmap")
    plt.xlabel("Digit")
    plt.ylabel("Digit")
    plt.tight_layout()
    plt.show()
