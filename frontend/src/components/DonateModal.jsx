// DonateModal.jsx
// /Users/apichet/quantum_lotto/frontend/src/components/DonateModal.jsx
// DonateModal.jsx (ใช้ promptpay.io)
import { useEffect, useMemo, useState } from "react";

function normalizeId(ppId) {
  // เก็บไว้เฉพาะตัวเลข (รองรับรูปแบบมีขีด/ช่องว่าง)
  return (ppId || "").replace(/\D/g, "");
}

function buildPromptPayUrl(ppId, amount) {
  const id = normalizeId(ppId);
  const base = `https://promptpay.io/${id}.png`;
  if (amount && Number(amount) > 0) {
    // ธนาคารส่วนใหญ่ต้องการทศนิยม 2 ตำแหน่ง
    const amt = Number(amount).toFixed(2);
    return `${base}?amount=${encodeURIComponent(amt)}`;
  }
  return base;
}

export default function DonateModal({ open, onClose, ppId, defaultAmount = 20, onConfirm }) {
  const [amt, setAmt] = useState(defaultAmount);

  useEffect(() => {
    if (open) {
      try {
        window.dispatchEvent(new CustomEvent("donate_opened", { detail: { amount: amt, ppId } }));
      } catch {}
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.body.style.overflow = prev; };
  }, [open]);

  const qrUrl = useMemo(() => buildPromptPayUrl(ppId, amt), [ppId, amt]);

  if (!open) return null;

  const confirm = () => {
    try {
      window.dispatchEvent(new CustomEvent("donate_confirmed", { detail: { amount: amt, ppId } }));
    } catch {}
    onConfirm?.({ amount: amt, ppId });
    onClose?.();
  };

  return (
    <div
      style={{ position:"fixed", inset:0, background:"rgba(0,0,0,.45)", display:"flex",
               alignItems:"center", justifyContent:"center", zIndex:9999, padding:12 }}
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-label="donation-modal"
    >
      <div onClick={(e)=>e.stopPropagation()}
           style={{ background:"#fff", padding:16, borderRadius:12, width:380, maxWidth:"100%",
                    boxShadow:"0 10px 20px rgba(0,0,0,.1), 0 6px 6px rgba(0,0,0,.08)" }}>
        <div className="d-flex justify-content-between align-items-start">
          <h3 className="m-0">สนับสนุนโปรเจกต์ ☕️</h3>
          <button type="button" className="btn-close" aria-label="Close" onClick={onClose} />
        </div>

        <p className="mt-2 mb-3">สแกนด้วยแอปธนาคาร/TrueMoney เพื่อทิป <b>{amt} บาท</b></p>

        <div className="d-flex flex-wrap gap-2 mb-3">
          {[10,20,50,100].map(v=>(
            <button key={v}
              className={`btn btn-sm ${amt===v ? "btn-primary":"btn-outline-primary"}`}
              onClick={()=>setAmt(v)}
            >{v} บาท</button>
          ))}
          <input type="number" min="1" value={amt}
                 onChange={e=>setAmt(Math.max(1, Number(e.target.value||1)))}
                 className="form-control form-control-sm" style={{ width:110 }} aria-label="custom-amount" />
        </div>

        <div style={{ background:"#fff", padding:12, border:"1px solid #eee", borderRadius:8,
                      display:"grid", placeItems:"center" }}>
          {/* ใช้ QR จาก promptpay.io */}
          <img src={qrUrl} alt="PromptPay QR" width={210} height={210}
               style={{ imageRendering:"pixelated" }}
               onError={(e)=>{ e.currentTarget.alt="โหลด QR ไม่ได้"; }} />
        </div>

        <div className="d-flex justify-content-between mt-3">
          <div className="btn-group">
            <button className="btn btn-outline-secondary btn-sm"
                    onClick={()=>navigator.clipboard.writeText(normalizeId(ppId))}>
              คัดลอกหมายเลข
            </button>
            <button className="btn btn-outline-secondary btn-sm"
                    onClick={()=>navigator.clipboard.writeText(String(amt))}>
              คัดลอกยอด
            </button>
          </div>
          <button className="btn btn-success" onClick={confirm}>✅ ฉันจ่ายแล้ว</button>
        </div>

        <p style={{ fontSize:12, opacity:.75 }} className="mt-2 mb-0">
          *การทิปไม่ได้เพิ่มโอกาสถูกรางวัลนะครับ ขอบคุณมากที่ช่วยให้โปรเจกต์ไปต่อ 😊
        </p>
      </div>
    </div>
  );
}
