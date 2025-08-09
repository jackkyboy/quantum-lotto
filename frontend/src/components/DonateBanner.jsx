// /Users/apichet/quantum_lotto/frontend/src/components/DonateBanner.jsx
// /Users/apichet/quantum_lotto/frontend/src/components/DonateBanner.jsx
// /Users/apichet/quantum_lotto/frontend/src/components/DonateBanner.jsx
import React, { useEffect, useMemo, useState } from "react";
import DonateModal from "./DonateModal";

const DISMISS_KEY = "donate_banner_dismissed_until";
const VARIANT_KEY = "donate_banner_variant";

const VARIANTS = [
  "💖 ช่วยเลี้ยงค่าน้ำชา/ค่าเซิร์ฟเวอร์ 20 บาท ได้ไหมครับ? ขอบคุณมาก!",
  "🔮 ถ้าผลทำนายมีประโยชน์ ฝากทิป 20 บาท เป็นกำลังใจให้ทีมเล็ก ๆ หน่อยนะ",
  "☁️ ทิป 20 บาท = ค่า Cloud 6 นาที 😂 ขอบคุณที่ช่วยให้โปรเจกต์ไปต่อ!",
];

function pickVariant() {
  const stored = localStorage.getItem(VARIANT_KEY);
  if (stored) return Number(stored);
  const idx = Math.floor(Math.random() * VARIANTS.length);
  localStorage.setItem(VARIANT_KEY, String(idx));
  return idx;
}

export default function DonateBanner({
  amount = 20,
  hideDays = 30,
  ppId = "0961717604",
}) {
  const [visible, setVisible] = useState(false);
  const [open, setOpen] = useState(false);
  const [modalAmount, setModalAmount] = useState(amount);
  const variantIdx = useMemo(() => pickVariant(), []);

  useEffect(() => {
    const until = Number(localStorage.getItem(DISMISS_KEY) || 0);
    setVisible(Date.now() > until);
  }, []);

  // ฟังอีเวนต์จากภายนอก เช่นปุ่มใน toolbar
  useEffect(() => {
    const handler = (e) => {
      const detail = e?.detail || {};
      if (typeof detail.amount === "number") setModalAmount(detail.amount);
      else setModalAmount(amount);
      setOpen(true);
    };
    window.addEventListener("donate_opened", handler);
    return () => window.removeEventListener("donate_opened", handler);
  }, [amount]);

  const dismiss = (days) => {
    const until = Date.now() + days * 24 * 60 * 60 * 1000;
    localStorage.setItem(DISMISS_KEY, String(until));
    setVisible(false);
  };

  const text = VARIANTS[variantIdx].replace(/20/g, String(amount));

  return (
    <>
      {/* แบนเนอร์อาจถูกซ่อน แต่คอมโพเนนต์ยังอยู่เพื่อฟังอีเวนต์ */}
      {visible && (
        <div
          className="alert alert-warning d-flex align-items-center justify-content-between"
          role="region"
          aria-label="donation-banner"
          style={{ marginTop: 8, marginBottom: 8 }}
        >
          <div className="me-3">
            {text}{" "}
            <small className="text-muted ms-2">
              *การทิปไม่ได้เพิ่มโอกาสถูกรางวัลนะครับ
            </small>
          </div>

          <div className="d-flex align-items-center gap-2">
            <button
              className="btn btn-sm btn-primary"
              onClick={() => {
                setModalAmount(amount);
                try {
                  window.dispatchEvent(
                    new CustomEvent("donate_opened", {
                      detail: { from: "banner", amount, ppId },
                    })
                  );
                } catch {}
                setOpen(true);
              }}
            >
              💸 สนับสนุน {amount} บาท
            </button>

            <button
              className="btn btn-sm btn-outline-secondary"
              onClick={() => dismiss(1)}
              title="ซ่อน 1 วัน"
            >
              ภายหลัง
            </button>

            <button
              type="button"
              className="btn-close ms-2"
              aria-label="Close"
              onClick={() => dismiss(hideDays)}
              title={`ซ่อน ${hideDays} วัน`}
            />
          </div>
        </div>
      )}

      {/* Modal – เปิดได้ทั้งจากแบนเนอร์หรืออีเวนต์ภายนอก */}
      <DonateModal
        open={open}
        onClose={() => setOpen(false)}
        ppId={ppId}
        defaultAmount={modalAmount}
        onConfirm={({ amount: paid }) => {
          try {
            window.dispatchEvent(
              new CustomEvent("donate_confirmed", { detail: { amount: paid, ppId } })
            );
          } catch {}
        }}
      />
    </>
  );
}
