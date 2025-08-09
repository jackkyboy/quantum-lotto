import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

try:
    from umap import UMAP
    HAS_UMAP = True
except ImportError:
    HAS_UMAP = False

def visualize_latent_field(df_8d, method="umap"):
    features = df_8d[["d1", "d2", "d3", "freq", "entangle", "monthly", "sim_hit", "drift"]].values
    if method == "umap" and HAS_UMAP:
        reducer = UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
    else:
        reducer = PCA(n_components=2)

    coords = reducer.fit_transform(features)
    df_8d["x"] = coords[:, 0]
    df_8d["y"] = coords[:, 1]

    plt.figure(figsize=(10, 6))
    plt.scatter(df_8d["x"], df_8d["y"], c=df_8d["freq"], cmap="plasma", s=20)
    plt.colorbar(label="Freq Bias")
    plt.title("🌌 8D Latent Quantum Field")
    plt.xlabel("Latent Axis 1")
    plt.ylabel("Latent Axis 2")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()

    return df_8d
