# /Users/apichet/quantum_lotto/src/api/app.py
# /Users/apichet/quantum_lotto/src/api/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from data_loader import load_json_data
from run.run_particle import run_particle_prediction
from run.run_schrodinger import run_schrodinger_simulation
from run.run_visualizations import run_quantum_field_visualizations
from visualizer.particle_plot import plot_particle_field_heatmap
from utils.statistics import compute_entropy
from ml.features import add_date_features, add_digit_features
from ml.model_pipeline import run_ml_pipeline

import os

# ✅ Init FastAPI
app = FastAPI()

# ✅ CORS สำหรับ frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือเฉพาะ ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ โหลดข้อมูลเพียงครั้งเดียวเมื่อเริ่ม
df_expanded = load_json_data()
from fastapi import Body
from config import generate_seed_from_date, lock_seed

# 🎯 ทำนายเลขท้าย 2 ตัว (Particle Field)
@app.post("/predict-particle")
def predict_particle(draw_date: str = Body(..., embed=True)):
    """
    ตัวอย่าง body:
    {
        "draw_date": "2025-08-16"
    }
    """
    # สร้างและล็อก SEED จาก draw_date
    seed = generate_seed_from_date(draw_date)
    lock_seed(seed)

    result_df = run_particle_prediction(df_expanded, seed=seed)

    if "Ψ(n)" in result_df.columns:
        result_df = result_df.rename(columns={"Ψ(n)": "psi"})

    top_5 = result_df.head(5)[["number", "psi"]].to_dict(orient="records")
    top_10 = result_df.head(10)[["number", "psi"]].to_dict(orient="records")

    return {
        "draw_date": draw_date,
        "seed_used": seed,
        "prediction": top_5,
        "top10": top_10
    }



# 🎲 จำลอง Schrödinger Simulation
@app.post("/predict-schrodinger")
def predict_schrodinger():
    df_full = df_expanded[["3digits"]].dropna().copy()
    sim_results, sim_counter, hits = run_schrodinger_simulation(df_full)
    entropy_val = compute_entropy(sim_counter)
    top_10 = [{"number": num, "count": count} for num, count in sim_counter.most_common(10)]
    return {
        "top10": top_10,
        "hits": hits,
        "entropy": round(entropy_val, 4),
        "total_simulated": len(sim_results)
    }

# 🌌 แสดงผลควอนตัมฟิลด์ + collapse
@app.post("/visualize-quantum-field")
def visualize_quantum_field():
    df_qfield, top2_df, collapsed = run_quantum_field_visualizations()
    return {
        "collapsed": collapsed,
        "top2digit": top2_df.to_dict(orient="records"),
        "field_size": len(df_qfield)
    }

# 🤖 รัน ML Pipeline
@app.post("/run-ml")
def run_ml():
    df = df_expanded.copy()
    df = add_date_features(df)
    df = add_digit_features(df)
    accuracy_dict = run_ml_pipeline(df)
    return accuracy_dict


# 🖼️ เซฟและส่ง heatmap ของ Ψ(n)
@app.get("/particle-plot")
@app.post("/particle-plot")
def particle_plot():
    result_df = run_particle_prediction(df_expanded)
    filename = "particle_field_heatmap.png"
    image_path = plot_particle_field_heatmap(result_df, filename=filename)

    return FileResponse(
        path=image_path,
        media_type="image/png",
        filename=filename
    )
