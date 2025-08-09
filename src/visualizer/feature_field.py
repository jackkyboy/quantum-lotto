import numpy as np
import pandas as pd
from collections import Counter
from utils.statistics import normalize_freq

def build_feature_8d_field(df, sim_hit_counter=None, drift_score=None, monthly_map=None):
    all_numbers = [f"{i:03d}" for i in range(1000)]
    freq_map = normalize_freq(Counter(df["3digits"]))
    entangled_digits = ['3', '6', '8']
    entangled_score = {n: sum(d in n for d in entangled_digits) for n in all_numbers}

    if monthly_map is None:
        monthly_map = {}
    monthly_bias = {n: 1.5 if n in set(monthly_map.values()) else 1.0 for n in all_numbers}

    sim_hit = sim_hit_counter or {}
    drift = drift_score or {}

    data = []
    for n in all_numbers:
        d1, d2, d3 = [int(d) for d in n]
        row = [
            n, d1, d2, d3,
            freq_map.get(n, 0),
            entangled_score.get(n, 0),
            monthly_bias.get(n, 1.0),
            sim_hit.get(n, 0),
            drift.get(n, 0)
        ]
        data.append(row)

    columns = ["number", "d1", "d2", "d3", "freq", "entangle", "monthly", "sim_hit", "drift"]
    return pd.DataFrame(data, columns=columns)
