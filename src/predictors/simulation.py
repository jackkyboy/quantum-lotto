from collections import Counter
from predictors.schrodinger import generate_schrodinger_superposition
import numpy as np

def run_schr_simulations(k=100000, top_k=20, seed=1234):
    samples = generate_schrodinger_superposition(k=k, seed=seed)
    counter = Counter(samples)
    return counter.most_common(top_k)

def multi_run_stability(n_runs=50, k_each=5, seed=999):
    np.random.seed(seed)
    all_results = []
    for _ in range(n_runs):
        batch = generate_schrodinger_superposition(k=k_each)
        all_results.extend(batch)
    return Counter(all_results).most_common(10)
