// /Users/apichet/quantum_lotto/frontend/src/App.jsx
// /Users/apichet/quantum_lotto/frontend/src/App.jsx
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

import Header from './components/Header';
import PredictionPanel from './components/PredictionPanel';
import MLReportCard from './components/MLReportCard';
import ParticleTable from './components/ParticleTable';
import DonateBanner from './components/DonateBanner';
import Footer from './components/Footer';
// ใน App.jsx
import HowToModal from './components/HowToModal';


function App() {
  const [predictions, setPredictions] = useState([]);
  const [particleTable, setParticleTable] = useState([]);
  const [schrodingerResults, setSchrodingerResults] = useState([]);
  const [mlAccuracy, setMLAccuracy] = useState({});
  const [heatmapUrl, setHeatmapUrl] = useState(null);
  const [drawDate, setDrawDate] = useState(localStorage.getItem('drawDate') || '');
  const [loadingPredict, setLoadingPredict] = useState(false);
  const [loadingSim, setLoadingSim] = useState(false);
  const [loadingML, setLoadingML] = useState(false);
  const [loadingHeatmap, setLoadingHeatmap] = useState(false);
  const [howToOpen, setHowToOpen] = useState(false);


  // meta จาก /predict-particle
  const [predictionMeta, setPredictionMeta] = useState({
    actual: null,
    hit5: false,
    hit10: false,
  });

  const API_BASE = "http://localhost:8000";

  useEffect(() => {
    localStorage.setItem('drawDate', drawDate || '');
  }, [drawDate]);

  const fetchPredictions = async () => {
    if (!drawDate) {
      alert("⚠️ กรุณาเลือกวันที่งวดก่อนรันทำนาย");
      return;
    }
    // ตรวจรูปแบบ YYYY-MM-DD แบบง่าย ๆ กัน 422
    if (!/^\d{4}-\d{2}-\d{2}$/.test(drawDate)) {
      alert("รูปแบบวันที่ไม่ถูกต้อง (ต้องเป็น YYYY-MM-DD)");
      return;
    }

    try {
      setLoadingPredict(true);
      const res = await axios.post(`${API_BASE}/predict-particle`, { draw_date: drawDate });
      // ตรวจว่าได้ object จริงไหม
      if (!res || !res.data) throw new Error("Empty response");

      setPredictions(res.data.prediction || []);
      setParticleTable(res.data.top10 || []);
      setPredictionMeta({
        actual: res.data.actual || null,
        hit5: !!res.data.hit5,
        hit10: !!res.data.hit10,
      });
    } catch (err) {
      // โชว์รายละเอียดจาก FastAPI ถ้ามี
      const msg =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        err?.message ||
        "เกิดข้อผิดพลาดในการทำนาย";
      console.error("❌ Error fetching predictions:", err);
      alert(msg);
    } finally {
      setLoadingPredict(false);
    }
  };


  const fetchSimulation = async () => {
    try {
      setLoadingSim(true);
      const body = drawDate ? { draw_date: drawDate } : {};
      const res = await axios.post(`${API_BASE}/predict-schrodinger`, body);
      setSchrodingerResults(res.data.top10 || []);
    } catch (err) {
      console.error("❌ Error fetching simulation:", err);
      alert("รันจำลองไม่สำเร็จ");
    } finally {
      setLoadingSim(false);
    }
  };

  const fetchMLAccuracy = async () => {
    try {
      setLoadingML(true);
      const res = await axios.post(`${API_BASE}/run-ml`);
      setMLAccuracy(res.data || {});
    } catch (err) {
      console.error("❌ Error fetching ML accuracy:", err);
      alert("รัน ML Pipeline ไม่สำเร็จ");
    } finally {
      setLoadingML(false);
    }
  };

  const fetchParticleHeatmap = async () => {
    try {
      setLoadingHeatmap(true);
      const t = Date.now();
      const url = drawDate
        ? `${API_BASE}/particle-plot?draw_date=${encodeURIComponent(drawDate)}&t=${t}`
        : `${API_BASE}/particle-plot?t=${t}`;
      setHeatmapUrl(url);
    } finally {
      setLoadingHeatmap(false);
    }
  };
  return (
    <div className="App container py-4">
      <Header />

      {/* Hero Section */}
      <div className="hero text-center mb-3">
        <h1>🧬 Quantum Lotto</h1>
        <div className="hero-sub">
          เมื่อกฎของควอนตัมมาบรรจบกับพลังของแมชชีนเลิร์นนิง<br/>
          เพื่อไขรหัสความน่าจะเป็นจากจักรวาลตัวเลข
        </div>
      </div>

      {/* Donate Banner (ชัดเจน ใต้ Hero) */}
      <div className="banner" role="region" aria-label="donation-banner">
        <DonateBanner amount={20} ppId="0961717604" />
      </div>

      {/* Toolbar: note (ซ้าย) + วิธีใช้งาน/ปุ่มโดเนทสำรอง (ขวา) */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <small className="text-muted">
          *เพื่อความบันเทิงและการทดลองเท่านั้น
        </small>
        <div className="d-flex gap-2">
          {/* ปุ่มโดเนทสำรอง (กันผู้ใช้เลื่อนผ่านแบนเนอร์) */}
          <button
            className="btn btn-sm btn-warning"
            onClick={() => window.dispatchEvent(new CustomEvent("donate_opened", { detail: { from: "toolbar", amount: 20 } }))}
            title="สนับสนุน 20 บาท"
          >
            💸 สนับสนุน 20 บาท
          </button>
          <button
            className="btn btn-outline-info btn-sm"
            onClick={() => setHowToOpen(true)}
            onKeyDown={(e) => (e.key === 'Enter' ? setHowToOpen(true) : null)}
            aria-label="เปิดวิธีใช้งาน"
            title="วิธีใช้งาน"
          >
            ℹ️ วิธีใช้งาน
          </button>
        </div>
      </div>



      {/* How-To Modal */}
      <HowToModal open={howToOpen} onClose={() => setHowToOpen(false)} />

      {/* Prediction Section */}
      <div className="section-card">
        <div className="section-title">🔮 ทำนายเลขท้าย 2 ตัว</div>
        <div className="controls mb-2 d-flex gap-2 flex-wrap">
          <input
            type="date"
            className="form-control"
            value={drawDate}
            onChange={(e) => setDrawDate(e.target.value)}
            placeholder="เลือกวันที่งวด"
            style={{ maxWidth: 220 }}
          />
          <button
            className="btn btn-primary"
            onClick={fetchPredictions}
            disabled={loadingPredict}
          >
            🎯 {loadingPredict ? <>กำลังทำนาย <span className="spinner-border spinner-border-sm inline-spinner" /></> : "รันทำนาย"}
          </button>
          <button
            className="btn btn-outline-secondary"
            onClick={fetchSimulation}
            disabled={loadingSim}
          >
            🧪 {loadingSim ? <>กำลังรัน <span className="spinner-border spinner-border-sm inline-spinner" /></> : "รัน Schrödinger"}
          </button>
        </div>

        <PredictionPanel predictions={predictions} />

        {/* แสดงสรุป hit5/hit10 */}
        {(predictionMeta.actual || predictionMeta.hit5 || predictionMeta.hit10) && (
          <div className="mt-2">
            <span className={`badge me-2 ${predictionMeta.hit5 ? "bg-success" : "bg-secondary"}`}>
              Top5 {predictionMeta.hit5 ? "✅" : "—"}
            </span>
            <span className={`badge me-2 ${predictionMeta.hit10 ? "bg-success" : "bg-secondary"}`}>
              Top10 {predictionMeta.hit10 ? "✅" : "—"}
            </span>
            {predictionMeta.actual && (
              <span className="badge bg-dark">ผลจริง {predictionMeta.actual}</span>
            )}
          </div>
        )}
      </div>

      {/* Schrödinger Results */}
      <div className="section-card">
        <div className="section-title">📊 ผลจำลอง Schrödinger</div>
        <ul className="list-group">
          {schrodingerResults.length === 0 && (
            <li className="list-group-item text-muted">ยังไม่มีข้อมูล</li>
          )}
          {schrodingerResults.map((item, i) => (
            <li key={i} className="list-group-item d-flex justify-content-between">
              <span>{item.number}</span>
              <span className="badge bg-dark">{item.count} ครั้ง</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Particle Field Table */}
      <div className="section-card">
        <div className="section-title">🧬 ตารางความน่าจะเป็นควอนตัม</div>
        <ParticleTable data={particleTable} />
      </div>

      {/* Heatmap */}
      <div className="section-card">
        <div className="section-title">📈 Ψ(n) Heatmap</div>
        <button
          className="btn btn-warning mb-2"
          onClick={fetchParticleHeatmap}
          disabled={loadingHeatmap}
        >
          🔥 {loadingHeatmap ? <>กำลังโหลด <span className="spinner-border spinner-border-sm inline-spinner" /></> : "โหลด Heatmap"}
        </button>
        {heatmapUrl ? (
          <div className="heatmap-box">
            <img src={heatmapUrl} alt="Heatmap" />
          </div>
        ) : (
          <div className="text-muted">ยังไม่มีภาพ</div>
        )}
      </div>

      {/* ML Accuracy */}
      <div className="section-card">
        <div className="section-title">🤖 ความแม่น ML</div>
        <button
          className="btn btn-success mb-3"
          onClick={fetchMLAccuracy}
          disabled={loadingML}
        >
          🧠 {loadingML ? <>กำลังรัน <span className="spinner-border spinner-border-sm inline-spinner" /></> : "รัน ML Pipeline"}
        </button>
        <MLReportCard accuracy={mlAccuracy} />
      </div>

      <Footer />
    </div>
  );

}

export default App;
