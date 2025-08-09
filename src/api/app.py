# /Users/apichet/quantum_lotto/src/api/app.py
# /Users/apichet/quantum_lotto/src/api/app.py
# /Users/apichet/quantum_lotto/src/api/app.py
# /Users/apichet/quantum_lotto/src/api/app.py

import os
import secrets
import pandas as pd
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Body, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import func, and_

from dotenv import load_dotenv
load_dotenv()  # ✅ โหลดค่าจาก .env ก่อน import module อื่นๆ

from data_loader import load_json_data
from run.run_particle import run_particle_prediction
from run.run_schrodinger import run_schrodinger_simulation
from run.run_visualizations import run_quantum_field_visualizations
from visualizer.particle_plot import plot_particle_field_heatmap
from utils.statistics import compute_entropy
from ml.features import add_date_features, add_digit_features
from ml.model_pipeline import run_ml_pipeline
from config import generate_seed_from_date, make_rngs

# Logging (SQLite/Postgres)
from storage.db import init_db, log_prediction, SessionLocal, PredictionLog
import json as _json

# -----------------------------
# App setup
# -----------------------------
init_db()
app = FastAPI()

# ✅ โหลด origins จาก .env
origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["http://localhost:3000"],  # fallback localhost
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# โหลดข้อมูลครั้งเดียว
df_expanded = load_json_data()

# -----------------------------
# Helpers
# -----------------------------
def _parse_draw_date_or_400(draw_date: str) -> str:
    try:
        dt = datetime.strptime(draw_date, "%Y-%m-%d").date()
        return dt.isoformat()
    except ValueError:
        raise HTTPException(status_code=400, detail="รูปแบบวันที่ต้องเป็น YYYY-MM-DD")


# แทนที่เดิม
def _find_actual_last2_for_date(draw_date_iso: str) -> Optional[str]:
    try:
        if "date" not in df_expanded.columns:
            return None
        # หา “งวดล่าสุดที่ <= draw_date”
        df_dates = df_expanded[df_expanded["date"].notna()].copy()
        df_dates["d"] = df_dates["date"].astype("datetime64[ns]")
        target = pd.to_datetime(draw_date_iso)
        df_on_or_before = df_dates[df_dates["d"] <= target]
        if df_on_or_before.empty:
            return None
        # เลือกแถวล่าสุด
        row = df_on_or_before.sort_values("d").iloc[-1]
        if "last2" in df_expanded.columns:
            return str(row["last2"]).zfill(2)
        if "3digits" in df_expanded.columns and pd.notna(row["3digits"]):
            return str(row["3digits"])[-2:].zfill(2)
    except Exception:
        return None
    return None



def _find_actual_3digits_for_date(draw_date_iso: str) -> list:
    out = []
    try:
        if "date" not in df_expanded.columns:
            return out
        df_dates = df_expanded[df_expanded["date"].notna()].copy()
        df_dates["d"] = df_dates["date"].astype("datetime64[ns]")
        target = pd.to_datetime(draw_date_iso)
        df_on_or_before = df_dates[df_dates["d"] <= target]
        if df_on_or_before.empty:
            return out
        row = df_on_or_before.sort_values("d").iloc[-1]
        # เก็บ 3digits ตามที่ dataset มี
        if "3digits" in df_expanded.columns and pd.notna(row["3digits"]):
            out.append(str(row["3digits"]).zfill(3))
        cols = [c for c in ["front3_1","front3_2","last3_1","last3_2","last3_3"] if c in df_expanded.columns]
        for c in cols:
            v = str(row[c])
            if v and v != "nan":
                out.append(v.zfill(3))
    except Exception:
        return out
    # unique
    seen, uniq = set(), []
    for v in out:
        if v and v not in seen:
            uniq.append(v); seen.add(v)
    return uniq



# ใน api/app.py
from sqlalchemy import and_
import json as _json

@app.post("/reconcile-logs")
def reconcile_logs():
    sess = SessionLocal()
    try:
        q = sess.query(PredictionLog).filter(
            and_(PredictionLog.actual == None, PredictionLog.draw_date != None)
        ).all()
        updated = 0
        for r in q:
            dd = r.draw_date
            # หา actual ใหม่
            if r.model == "particle":
                actual = _find_actual_last2_for_date(dd)
                if actual:
                    topn = _json.loads(r.topn or "[]")
                    pred_set = {str(x.get("number")).zfill(2) for x in topn if "number" in x}
                    r.actual = actual
                    r.hit = actual in pred_set
                    updated += 1
            elif r.model == "schrodinger":
                actuals = _find_actual_3digits_for_date(dd)
                if actuals:
                    topn = _json.loads(r.topn or "[]")
                    pred_set = {str(x.get("number")).zfill(3) for x in topn if "number" in x}
                    r.actual = ",".join(actuals)
                    r.hit = any(a in pred_set for a in actuals)
                    updated += 1
        sess.commit()
        return {"updated": updated}
    finally:
        sess.close()

# -----------------------------
# Endpoints
# -----------------------------
# 🎯 ทำนายเลขท้าย 2 ตัว (Particle Field)
@app.post("/predict-particle")
def predict_particle(draw_date: str = Body(..., embed=True)):
    """
    Body ตัวอย่าง:
    { "draw_date": "2025-08-16" }
    """
    draw_date_iso = _parse_draw_date_or_400(draw_date)

    # สร้าง seed + local RNG
    seed = generate_seed_from_date(draw_date_iso)
    _, np_rng = make_rngs(seed)

    # รันทำนาย (ขอ metrics กลับมาด้วย)
    result_df, picks, metrics = run_particle_prediction(
        df_expanded, np_rng=np_rng, save_image=False, return_metrics=True
    )

    # ให้แน่ใจว่ามี psi
    if "Ψ(n)" in result_df.columns and "psi" not in result_df.columns:
        result_df = result_df.rename(columns={"Ψ(n)": "psi"})
    if "psi" in result_df.columns:
        result_df = result_df.sort_values("psi", ascending=False).reset_index(drop=True)

    top_5 = result_df.head(5)[["number", "psi"]].to_dict(orient="records")
    top_10 = result_df.head(10)[["number", "psi"]].to_dict(orient="records")

    # ใช้ actual/hit5/hit10 จาก metrics ถ้ามี
    actual_last2 = metrics["actual"] if metrics else _find_actual_last2_for_date(draw_date_iso)
    hit5 = bool(metrics and metrics.get("hit5"))
    hit10 = bool(metrics and metrics.get("hit10"))
    # ถ้า metrics ไม่มี ให้คำนวณสำรองจากตาราง
    if not metrics and actual_last2:
        pred5_set = {str(x["number"]).zfill(2) for x in top_5}
        pred10_set = {str(x["number"]).zfill(2) for x in top_10}
        hit5 = actual_last2 in pred5_set
        hit10 = actual_last2 in pred10_set

    # บันทึก Log (นับหลักตาม Top10)
    try:
        log_prediction(
            draw_date=draw_date_iso,
            model="particle",
            feature=f"particle_field|hit5={int(hit5)}|hit10={int(hit10)}",
            seed=seed,
            picks=[x["number"] for x in top_5],
            topn=top_10,
            actual=actual_last2,
            hit=hit10
        )
    except Exception as e:
        print("⚠️ log_prediction particle error:", repr(e))

    return {
        "draw_date": draw_date_iso,
        "seed_used": seed,
        "prediction": top_5,
        "top10": top_10,
        "actual": actual_last2,
        "hit5": hit5,
        "hit10": hit10,
        "hit": hit10,  # คงนิยามหลักตาม Top10
    }


# 🎲 Schrödinger Simulation
@app.post("/predict-schrodinger")
def predict_schrodinger(draw_date: Optional[str] = Body(None, embed=True)):
    if draw_date:
        draw_date_iso = _parse_draw_date_or_400(draw_date)
        seed = generate_seed_from_date(draw_date_iso)
    else:
        draw_date_iso = None
        seed = secrets.randbits(32)

    _, np_rng = make_rngs(seed)

    df_full = df_expanded[["3digits"]].dropna().copy() if "3digits" in df_expanded.columns else df_expanded.copy()
    sim_results, sim_counter, hits = run_schrodinger_simulation(df_full, np_rng=np_rng)
    entropy_val = compute_entropy(sim_counter)
    top_10 = [{"number": num, "count": count} for num, count in sim_counter.most_common(10)]

    # หา actual 3digits และ log
    actual_3digits = _find_actual_3digits_for_date(draw_date_iso) if draw_date_iso else []
    pred_set = {x["number"] for x in top_10}
    hit = any(a in pred_set for a in actual_3digits) if actual_3digits else False

    try:
        log_prediction(
            draw_date=draw_date_iso,
            model="schrodinger",
            feature="stochastic_optimal+superposition",
            seed=seed,
            picks=[x["number"] for x in top_10[:5]],
            topn=top_10,
            actual=",".join(actual_3digits) if actual_3digits else None,
            hit=hit
        )
    except Exception as e:
        print("⚠️ log_prediction schrodinger error:", repr(e))

    return {
        "draw_date": draw_date_iso,
        "seed_used": seed,
        "top10": top_10,
        "hits": hits,
        "entropy": round(entropy_val, 4),
        "total_simulated": len(sim_results),
        "actual": actual_3digits or None,
        "hit": hit
    }



# 🌌 Visualization (คงเดิม)
@app.post("/visualize-quantum-field")
def visualize_quantum_field():
    df_qfield, top2_df, collapsed = run_quantum_field_visualizations()
    return {
        "collapsed": collapsed,
        "top2digit": top2_df.to_dict(orient="records"),
        "field_size": len(df_qfield)
    }


# 🤖 ML Pipeline (คงเดิม)
@app.post("/run-ml")
def run_ml():
    df = df_expanded.copy()
    df = add_date_features(df)
    df = add_digit_features(df)
    accuracy_dict = run_ml_pipeline(df)
    return accuracy_dict


# 🖼️ Ψ(n) Heatmap
@app.get("/particle-plot")
@app.post("/particle-plot")
def particle_plot(draw_date: Optional[str] = Query(default=None)):
    if draw_date:
        draw_date_iso = _parse_draw_date_or_400(draw_date)
        seed = generate_seed_from_date(draw_date_iso)
    else:
        # ใช้งวดล่าสุดเป็น seed ถ้ามี
        if "date" in df_expanded.columns and df_expanded["date"].notna().any():
            latest_date = str(df_expanded["date"].dropna().max())
            seed = generate_seed_from_date(str(latest_date))
        else:
            seed = 42

    _, np_rng = make_rngs(seed)

    result_df, _ = run_particle_prediction(df_expanded, np_rng=np_rng, save_image=False)

    # ให้ plot รองรับทั้ง 'psi' และ 'Ψ(n)'
    if "psi" in result_df.columns and "Ψ(n)" not in result_df.columns:
        result_df_plot = result_df.rename(columns={"psi": "Ψ(n)"})
    else:
        result_df_plot = result_df

    filename = "particle_field_heatmap.png"
    image_path = plot_particle_field_heatmap(result_df_plot, filename=filename)

    return FileResponse(
        path=image_path,
        media_type="image/png",
        filename=filename
    )


# 📈 สรุปสถิติการทำนาย
@app.get("/prediction-stats")
def prediction_stats(model: Optional[str] = Query(default=None)):
    sess = SessionLocal()
    try:
        q = sess.query(PredictionLog)
        if model:
            q = q.filter(PredictionLog.model == model)

        total = q.count()
        hits = q.filter(PredictionLog.hit == True).count()

        # นับ streak ล่าสุด (เรียงจากล่าสุด)
        streak = 0
        for rec in q.order_by(PredictionLog.created_at.desc()).all():
            if rec.hit:
                streak += 1
            else:
                break

        # by model (คำนวณฝั่ง Python ให้ชัวร์)
        agg = {}
        for m in ["particle", "schrodinger"]:
            m_q = sess.query(PredictionLog).filter(PredictionLog.model == m).all()
            agg[m] = {
                "total": len(m_q),
                "hits": sum(1 for r in m_q if r.hit)
            }

        return {
            "total": total,
            "hits": hits,
            "hit_rate": round(hits / total, 4) if total else 0.0,
            "current_streak": streak,
            "by_model": agg
        }
    finally:
        sess.close()


# 🧾 ประวัติการทำนายล่าสุด
@app.get("/prediction-logs")
def prediction_logs(limit: int = 50):
    import json as _json
    sess = SessionLocal()
    try:
        q = (
            sess.query(PredictionLog)
            .order_by(PredictionLog.created_at.desc())
            .limit(limit)
            .all()
        )
        out = []
        for r in q:
            out.append({
                "id": r.id,
                "created_at": r.created_at.isoformat(),
                "draw_date": r.draw_date,
                "model": r.model,
                "feature": r.feature,
                "seed": r.seed,
                "picks": _json.loads(r.picks or "[]"),
                "topn": _json.loads(r.topn or "[]"),
                "actual": r.actual,
                "hit": bool(r.hit),
            })
        return out
    finally:
        sess.close()
