# /Users/apichet/quantum_lotto/src/api/app.py
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from data_loader import load_json_data
from run.run_particle import run_particle_prediction
from run.run_schrodinger import run_schrodinger_simulation
from run.run_visualizations import run_quantum_field_visualizations
from visualizer.particle_plot import plot_particle_field_heatmap
from utils.statistics import compute_entropy
from ml.features import add_date_features, add_digit_features
from ml.model_pipeline import run_ml_pipeline
from config import generate_seed_from_date, lock_seed

import os

app = FastAPI(title="Quantum Lotto API")

# ===== CORS: allow Firebase Hosting + local dev =====
ALLOWED_ORIGINS = [
    "https://quantum-lotto.web.app",
    "https://quantum-lotto.firebaseapp.com",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ===== Healthcheck / root =====
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"name": "Quantum Lotto API", "health": "ok"}

# ===== Load data once on startup =====
df_expanded = load_json_data()
# ===== Particle Prediction =====
@app.post("/predict-particle")
def predict_particle(draw_date: str = Body(..., embed=True)):
    """
    Body:
    { "draw_date": "YYYY-MM-DD" }
    """
    try:
        if not draw_date or len(draw_date) < 8:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid draw_date")

        # 🔐 ล็อก seed ให้ deterministic
        seed = generate_seed_from_date(draw_date)
        lock_seed(seed)

        # 👇 ไม่ส่ง seed เข้าไป (ฟังก์ชันไม่รองรับ keyword นี้)
        result_df = run_particle_prediction(df_expanded)

        # map ชื่อคอลัมน์ ถ้ามี Ψ(n)
        if "Ψ(n)" in result_df.columns:
            result_df = result_df.rename(columns={"Ψ(n)": "psi"})

        # สร้างผลลัพธ์ top 5 / top 10
        top_5 = result_df.head(5)[["number", "psi"]].to_dict(orient="records")
        top_10 = result_df.head(10)[["number", "psi"]].to_dict(orient="records")

        return {
            "draw_date": draw_date,
            "seed_used": seed,
            "prediction": top_5,
            "top10": top_10
        }
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "predict-particle failed", "detail": str(e)}
        )


# ===== Schrödinger Simulation =====
@app.post("/predict-schrodinger")
def predict_schrodinger():
    try:
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
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "predict-schrodinger failed", "detail": str(e)}
        )

# ===== Quantum Field Visualization =====
@app.post("/visualize-quantum-field")
def visualize_quantum_field():
    try:
        df_qfield, top2_df, collapsed = run_quantum_field_visualizations()
        return {
            "collapsed": collapsed,
            "top2digit": top2_df.to_dict(orient="records"),
            "field_size": len(df_qfield)
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "visualize-quantum-field failed", "detail": str(e)}
        )

# ===== ML Pipeline =====
@app.post("/run-ml")
def run_ml():
    try:
        df = df_expanded.copy()
        df = add_date_features(df)
        df = add_digit_features(df)
        accuracy_dict = run_ml_pipeline(df)
        return accuracy_dict
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "run-ml failed", "detail": str(e)}
        )

# ===== Particle heatmap =====
@app.get("/particle-plot")
@app.post("/particle-plot")
def particle_plot():
    try:
        result_df = run_particle_prediction(df_expanded)
        filename = "particle_field_heatmap.png"
        image_path = plot_particle_field_heatmap(result_df, filename=filename)
        return FileResponse(path=image_path, media_type="image/png", filename=filename)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "particle-plot failed", "detail": str(e)}
        )
