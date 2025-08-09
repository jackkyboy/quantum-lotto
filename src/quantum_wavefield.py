# quantum_wavefield.py

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

# 🌀 สร้างคลื่นควอนตัมจากหลาย bias แล้วคำนวณความน่าจะเป็น (likelihood)
def generate_quantum_likelihood_field(
    freq_bias=None,
    schr_bias=None,
    interf_bias=None,
    monthly_bias=None,
    blackhole_boost=None,
    overused_penalty=None,
    phase_config=None,
    seed=42,
    return_top=20
):
    """
    ผสมคลื่น bias หลายแหล่งพร้อม phase แล้วทำ normalization
    Return: DataFrame พร้อม PCA coords และ Quantum Likelihood
    """
    np.random.seed(seed)

    all_numbers = [f"{i:03d}" for i in range(1000)]
    vectors = np.array([[int(d) for d in num] for num in all_numbers])

    # ใช้ค่า default ถ้ายังไม่มี
    if freq_bias is None:
        freq_bias = np.random.rand(1000)
    if schr_bias is None:
        schr_bias = np.zeros(1000)
        schr_bias[np.random.choice(1000, 50, replace=False)] = 1.5
    if interf_bias is None:
        interf_bias = np.zeros(1000)
        interf_bias[np.random.choice(1000, 50, replace=False)] = 1.3
    if monthly_bias is None:
        monthly_bias = np.zeros(1000)
        monthly_bias[np.random.choice(1000, 100, replace=False)] = 1.2
    if blackhole_boost is None:
        blackhole_boost = np.zeros(1000)
        blackhole_boost[np.random.choice(1000, 10, replace=False)] = 2.0
    if overused_penalty is None:
        overused_penalty = np.ones(1000)
        overused_penalty[np.random.choice(1000, 50, replace=False)] = 0.5

    # กำหนด phase (default)
    if phase_config is None:
        phase_config = {
            "freq": 0,
            "schr": np.pi/4,
            "interf": np.pi/2,
            "monthly": np.pi,
            "blackhole": -np.pi/2,
            "overused": np.pi
        }

    # 🧮 สร้าง complex amplitude wave แต่ละแหล่ง
    freq_amp = freq_bias * np.exp(1j * phase_config["freq"])
    schr_amp = schr_bias * np.exp(1j * phase_config["schr"])
    interf_amp = interf_bias * np.exp(1j * phase_config["interf"])
    monthly_amp = monthly_bias * np.exp(1j * phase_config["monthly"])
    blackhole_amp = blackhole_boost * np.exp(1j * phase_config["blackhole"])
    overused_amp = overused_penalty * np.exp(1j * phase_config["overused"])

    # 🔁 รวมทั้งหมดเป็น superposed wave
    combined_amp = (
        freq_amp +
        schr_amp +
        interf_amp +
        monthly_amp +
        blackhole_amp +
        overused_amp
    )

    # ✂️ Normalize
    combined_amp /= np.linalg.norm(combined_amp)
    likelihoods = np.abs(combined_amp) ** 2

    # 📊 ทำ PCA สำหรับการมองใน latent space
    pca = PCA(n_components=2)
    components = pca.fit_transform(vectors)

    df_quantum = pd.DataFrame({
        "number": all_numbers,
        "pca_x": components[:, 0],
        "pca_y": components[:, 1],
        "likelihood": likelihoods
    })

    top_quantum = df_quantum.sort_values("likelihood", ascending=False).head(return_top)
    return df_quantum, top_quantum
