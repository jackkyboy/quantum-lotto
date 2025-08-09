# /Users/apichet/quantum_lotto/src/run/run_visualizations.py

# /Users/apichet/quantum_lotto/src/run/run_visualizations.py
# /Users/apichet/quantum_lotto/src/run/run_visualizations.py

# ============================================
# 🛠 Path Fix (เพื่อให้ import จาก src ได้)
# ============================================
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ============================================
# 🔧 Imports (หลังจากแก้ path แล้ว)
# ============================================
from visualization.quantum_viz import (
    collapse_from_quantum_field,
    visualize_quantum_field_and_superposition,
    visualize_digit_entanglement,
    extract_top_2digit_from_qfield
)
from quantum_wavefield import generate_quantum_likelihood_field
from config import generate_seed_from_date, make_rngs  # ✅ ใช้ local RNG แทน lock_seed

from datetime import datetime
from typing import Optional


# ============================================
# 🎯 Main Visualization Runner
# ============================================
def run_quantum_field_visualizations(draw_date: Optional[str] = None, seed: Optional[int] = None, np_rng=None):
    """
    รันชุดการแสดงภาพของ Quantum Field:
    - Likelihood Field
    - Collapse Simulation
    - Digit Entanglement Heatmap
    - Top 2-digit likelihood

    Parameters
    ----------
    draw_date : Optional[str]
        รูปแบบ 'YYYY-MM-DD' ถ้าส่งมาจะใช้สร้าง seed แบบ deterministic
    seed : Optional[int]
        ใช้แทน draw_date ได้ (ถ้าไม่ส่ง np_rng)
    np_rng : Optional[np.random.Generator]
        Local RNG ถ้ามีจะใช้ตัวนี้เป็นหลัก
    """
    # ✅ เตรียม RNG แบบ local
    if np_rng is None:
        if seed is None and draw_date:
            # แปลง draw_date -> seed
            try:
                dt = datetime.strptime(draw_date, "%Y-%m-%d").date()
                seed = generate_seed_from_date(dt.isoformat())
            except ValueError:
                raise ValueError("รูปแบบ draw_date ต้องเป็น YYYY-MM-DD")
        elif seed is None and not draw_date:
            # fallback ค่าคงที่ (ถ้าไม่ส่งอะไรมาเลย)
            seed = 42
        _, np_rng = make_rngs(seed)

    # ✅ สร้าง Quantum Field (พยายามส่ง np_rng ถ้าฟังก์ชันรองรับ)
    try:
        # ถ้า generate_quantum_likelihood_field รองรับ np_rng
        df_qfield, extra = generate_quantum_likelihood_field(np_rng=np_rng)
    except TypeError:
        # เวอร์ชันเดิมไม่รองรับ np_rng
        df_qfield, extra = generate_quantum_likelihood_field()

    # 🌌 1) Visualize Quantum Likelihood Field & Superposition Matrix
    visualize_quantum_field_and_superposition(df_qfield)

    # 🧠 2) Collapse Simulation → คัดเลือกเลขเด่น
    # พยายามใช้ np_rng ก่อน ถ้าไม่รองรับ ค่อยส่ง seed
    collapsed = None
    try:
        collapsed = collapse_from_quantum_field(df_qfield, n=5, np_rng=np_rng)
    except TypeError:
        try:
            # ใช้ seed จาก RNG เดิม (ดึงไม่ได้โดยตรง เลยใช้ค่าเริ่มสร้างแทน)
            collapsed = collapse_from_quantum_field(df_qfield, n=5, seed=seed if 'seed' in locals() else 42)
        except TypeError:
            # ไม่มีทั้ง np_rng/seed ใน signature
            collapsed = collapse_from_quantum_field(df_qfield, n=5)

    # 🧬 3) Heatmap การพัวพันของตัวเลข (Digit Entanglement)
    visualize_digit_entanglement(df_qfield)

    # 🔢 4) Extract เลข 2 ตัวท้ายที่เด่นที่สุด
    top_2digit_df = extract_top_2digit_from_qfield(df_qfield, top_n=10)

    return df_qfield, top_2digit_df, collapsed


# ============================================
# 🚀 CLI Entry Point
# ============================================
if __name__ == "__main__":
    # df_q, top2, collapsed = run_quantum_field_visualizations(draw_date="2025-08-16")
    df_q, top2, collapsed = run_quantum_field_visualizations(seed=20250816)

    print("\n🎯 Collapsed Numbers:", collapsed)
    print("\n🔝 Top 2-digit Numbers:\n", top2)
