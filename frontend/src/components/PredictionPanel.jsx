// src/components/PredictionPanel.jsx
import React, { useState } from 'react';
import axios from 'axios';

function PredictionPanel({ predictions, onUpdate }) {
  const [drawDate, setDrawDate] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchPredictions = async () => {
    if (!drawDate) {
      alert("⚠️ กรุณาเลือกวันที่ก่อนทำนาย");
      return;
    }

    try {
      setLoading(true);
      const res = await axios.post('http://localhost:8000/predict-particle', {
        draw_date: drawDate
      });

      onUpdate(res.data.prediction || []);
    } catch (err) {
      console.error("❌ Error fetching predictions:", err);
      alert("เกิดข้อผิดพลาดในการทำนาย");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-4">
      <h5>📅 กรุณาเลือกวันที่งวด:</h5>
      <input
        type="date"
        className="form-control mb-3"
        value={drawDate}
        onChange={(e) => setDrawDate(e.target.value)}
      />

      <button
        className="btn btn-primary mb-3"
        onClick={fetchPredictions}
        disabled={loading}
      >
        🎯 {loading ? "กำลังประมวลผล..." : "รันทำนาย"}
      </button>

      {predictions && predictions.length > 0 && (
        <>
          <h5>🔮 เลขที่ระบบแนะนำ (Top 5)</h5>
          <ul className="list-group">
            {predictions.map((item, index) => (
              <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
                <span>เลข {item.number}</span>
                <span className="badge bg-primary text-white">
                  Ψ(n): {item.psi?.toFixed(6) ?? 'N/A'}
                </span>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default PredictionPanel;
