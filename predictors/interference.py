import numpy as np
from collections import Counter
from utils.statistics import normalize_freq

def interference_sample(wave_base, entangled_digits=['3', '6', '8'], k=5, seed=None):
    """
    ✨ ชนคลื่นควอนตัมระหว่าง wave จาก frequency และ entangled-digit bias
    """
    if seed is not None:
        np.random.seed(seed)

    full_space = [f"{i:03d}" for i in range(1000)]

    wave_entangled = {}
    for num in full_space:
        ent_count = sum(d in num for d in entangled_digits)
        wave_entangled[num] = 1 + 0.25 * ent_count

    wave_entangled = normalize_freq(Counter(wave_entangled))

    interference_wave = {}
    for num in full_space:
        p1 = wave_base.get(num, 0)
        p2 = wave_entangled.get(num, 0)
        val = (p1 * p2) ** 0.5
        if val > 0:
            interference_wave[num] = val

    if not interference_wave:
        return []

    interference_wave = normalize_freq(Counter(interference_wave))
    keys = list(interference_wave.keys())
    probs = list(interference_wave.values())

    return np.random.choice(keys, size=min(k, len(keys)), replace=False, p=probs)



def generate_multi_wave_top_k(freq_wave, entangled_digits, monthly_bias, k=5):
    full_space = [f"{i:03d}" for i in range(1000)]
    amp = np.ones(1000)

    for idx, num in enumerate(full_space):
        amp[idx] *= freq_wave.get(num, 1e-6)
        amp[idx] *= (1 + 0.2 * sum([d in num for d in entangled_digits]))
        if num in set(monthly_bias.values()):
            amp[idx] *= 1.5

    amp /= amp.sum()
    return np.random.choice(full_space, size=k, replace=False, p=amp)
