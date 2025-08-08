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
from config import generate_seed_from_date, lock_seed



# ============================================
# 🎯 Main Visualization Runner
# ============================================
def run_quantum_field_visualizations():
    """
    รันชุดการแสดงภาพของ Quantum Field:
    - Likelihood Field
    - Collapse Simulation
    - Digit Entanglement Heatmap
    - Top 2-digit likelihood
    """
    # ✅ สร้าง Quantum Field
    df_qfield, _ = generate_quantum_likelihood_field()

    # 🌌 1. Visualize Quantum Likelihood Field & Superposition Matrix
    visualize_quantum_field_and_superposition(df_qfield)

    # 🧠 2. Collapse Simulation → คัดเลือกเลขเด่น
    collapsed = collapse_from_quantum_field(df_qfield, n=5, seed=GLOBAL_SEED)

    # 🧬 3. Heatmap การพัวพันของตัวเลข (Digit Entanglement)
    visualize_digit_entanglement(df_qfield)

    # 🔢 4. Extract เลข 2 ตัวท้ายที่เด่นที่สุด
    top_2digit_df = extract_top_2digit_from_qfield(df_qfield, top_n=10)

    return df_qfield, top_2digit_df, collapsed

# ============================================
# 🚀 CLI Entry Point
# ============================================
if __name__ == "__main__":
    df_q, top2, collapsed = run_quantum_field_visualizations()
    print("\n🎯 Collapsed Numbers:", collapsed)
    print("\n🔝 Top 2-digit Numbers:\n", top2)
