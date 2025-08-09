import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from typing import Dict, Tuple, List, Union

try:
    from umap import UMAP
    HAS_UMAP = True
except ImportError:
    HAS_UMAP = False

def encode_3digit_to_vector(num_str: Union[str, int]) -> List[int]:
    return [int(d) for d in str(num_str).zfill(3)]

def visualize_quantum_field(coords: List[List[float]], probs: List[float]):
    from mpl_toolkits.mplot3d import Axes3D
    x = [c[0] for c in coords]
    y = [c[1] for c in coords]
    z = probs
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(x, y, z, cmap='viridis', linewidth=0.2)
    ax.set_title("🌀 Quantum-Likelihood Field")
    ax.set_xlabel("Latent Axis 1")
    ax.set_ylabel("Latent Axis 2")
    ax.set_zlabel("Probability Amplitude")
    plt.tight_layout()
    plt.show()

def heatmap_quantum_valleys(coords: List[List[float]], probs: List[float]):
    df = pd.DataFrame(coords, columns=["x", "y"])
    df["prob"] = probs
    df["x_bin"] = df["x"].round(1)
    df["y_bin"] = df["y"].round(1)
    pivot = df.pivot_table(index="y_bin", columns="x_bin", values="prob", aggfunc="mean")
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot, cmap="viridis")
    plt.title("🌌 Quantum Probability Valleys")
    plt.xlabel("Latent Axis 1 (binned)")
    plt.ylabel("Latent Axis 2 (binned)")
    plt.tight_layout()
    plt.show()

def analyze_simulation_hits_with_embedding(
    hit_counter: Dict[str, int],
    top_n: int = 100,
    method: str = "pca",
    visualize: bool = True
) -> Tuple[List[List[float]], List[float]]:
    data = []
    for num, count in hit_counter.items():
        if count > 0:
            vec = encode_3digit_to_vector(num)
            data.append(vec + [count])
    if not data:
        return [], []

    df = pd.DataFrame(data, columns=["d1", "d2", "d3", "count"])
    df_top = df.sort_values("count", ascending=False).head(top_n)
    features = df_top[["d1", "d2", "d3"]].values

    if method == "umap" and HAS_UMAP:
        reducer = UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
        components = reducer.fit_transform(features)
    else:
        pca = PCA(n_components=2)
        components = pca.fit_transform(features)

    coords = components.tolist()
    probs = df_top["count"].values / df_top["count"].sum()

    if visualize:
        print(f"\n🔍 Visualizing using method: {method.upper()}")
        heatmap_quantum_valleys(coords, probs)
        visualize_quantum_field(coords, probs)

    return coords, probs
