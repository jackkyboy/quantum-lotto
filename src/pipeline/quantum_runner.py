# /Users/apichet/quantum_lotto/src/pipeline/quantum_runner.py
# /Users/apichet/quantum_lotto/src/pipeline/quantum_runner.py

from run.run_particle import run_particle_prediction
from run.run_schrodinger import run_schrodinger_simulation, run_unitary_collapse, run_backtest
from run.run_visualizations import run_quantum_field_visualizations
from ml.features import add_date_features, add_digit_features
from ml.model_pipeline import run_ml_pipeline
from config import make_rngs, generate_seed_from_date

from datetime import datetime


def _resolve_seed(draw_date: str | None, seed: int | None) -> int:
    """
    ตีความ seed:
    - ถ้ามี draw_date ใช้มันสร้าง seed (format: YYYY-MM-DD)
    - ถ้าไม่มี draw_date แต่มี seed -> ใช้ seed นั้น
    - ถ้าไม่มีทั้งคู่ -> ใช้ fallback = 42
    """
    if draw_date:
        try:
            dt = datetime.strptime(draw_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("รูปแบบ draw_date ต้องเป็น YYYY-MM-DD")
        return generate_seed_from_date(dt.isoformat())
    if seed is not None:
        return seed
    return 42  # fallback


def run_all_simulations(df, draw_date: str | None = None, seed: int | None = None, save_image: bool = False):
    """
    รันทุก pipeline แบบ deterministic ด้วย local RNG
    - df: DataFrame ข้อมูลหลัก
    - draw_date / seed: ระบุอย่างใดอย่างหนึ่งเพื่อ deterministic
    - save_image: ให้ run_particle_prediction เซฟ heatmap ไหม (ปกติ False เพื่อความเร็ว)
    """
    # ✅ สร้าง local RNG จาก seed
    seed_val = _resolve_seed(draw_date, seed)
    _, np_rng = make_rngs(seed_val)

    # ------------------------------
    # 1) Particle Prediction
    # ------------------------------
    result_df, picks = run_particle_prediction(df, np_rng=np_rng, save_image=save_image)
    # (ถ้าจะใช้ผลต่อ สามารถ return/บันทึกเพิ่มได้)

    # ------------------------------
    # 2) Schrödinger Simulation
    # ------------------------------
    # เตรียม df เฉพาะคอลัมน์ "3digits"
    if "3digits" in df.columns:
        df_full = df[["3digits"]].dropna().copy()
    else:
        df_full = df.copy()
    sim_results, sim_counter, hits = run_schrodinger_simulation(df_full, np_rng=np_rng)

    # Unitary collapse (ให้ deterministic ด้วย seed เดิม)
    run_unitary_collapse(seed=seed_val)

    # Backtest
    run_backtest(df_full)

    # ------------------------------
    # 3) Quantum Field Visualization
    # ------------------------------
    run_quantum_field_visualizations(seed=seed_val, np_rng=np_rng)

    # ------------------------------
    # 4) ML Pipeline
    # ------------------------------
    df_ml = add_date_features(df.copy())
    df_ml = add_digit_features(df_ml)
    run_ml_pipeline(df_ml)

    # ฟังก์ชันนี้ไม่ return ค่าเหมือนเดิม
