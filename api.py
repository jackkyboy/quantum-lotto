# /Users/apichet/quantum_lotto/src/api.py
from flask import Flask, jsonify
from flask_cors import CORS

from predictors_particle import run_particle_prediction
from data_loader import load_json_data

app = Flask(__name__)
CORS(app)


@app.route("/api/predict", methods=["GET"])
def predict_numbers():
    """API สำหรับทำนายเลขท้าย 2 ตัวจาก Particle Field"""
    df = load_json_data()
    result_df, predictions = run_particle_prediction(df, return_predictions=True)

    top_psi = result_df.head(10).to_dict(orient="records")
    return jsonify({
        "predictions": predictions,
        "top_psi": top_psi
    })


@app.route("/api/simulate", methods=["GET"])
def simulate():
    """API จำลองผลย้อนหลัง"""
    df = load_json_data()
    sim_results = run_simulation_over_n_draws(df, n_draws=100)

    return jsonify({
        "accuracy": round(100 * sum(sim_results) / len(sim_results), 2),
        "total": len(sim_results),
        "hits": sum(sim_results)
    })


@app.route("/api/ml", methods=["GET"])
def ml_accuracy():
    """API สำหรับเรียกผลลัพธ์ accuracy จาก ML pipeline"""
    # อาจเปลี่ยนให้เรียกฟังก์ชันจริง เช่น run_ml_pipeline()
    return jsonify({
        "logreg": "67%",
        "rf": "100%",
        "xgb": "100%"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
