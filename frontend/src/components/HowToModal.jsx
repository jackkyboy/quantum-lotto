// HowToModal.jsx
export default function HowToModal({ open, onClose }) {
  if (!open) return null;
  return (
    <div
      style={{position:'fixed', inset:0, background:'rgba(0,0,0,.45)', display:'flex', alignItems:'center', justifyContent:'center', zIndex:9999, padding:12}}
      onClick={onClose}
      role="dialog" aria-modal="true" aria-label="howto-modal"
    >
      <div onClick={(e)=>e.stopPropagation()} style={{background:'#fff', borderRadius:12, width:680, maxWidth:'100%', padding:20}}>
        <div className="d-flex justify-content-between align-items-start">
          <h3 className="m-0">วิธีใช้งาน Quantum Lotto</h3>
          <button type="button" className="btn-close" onClick={onClose} aria-label="Close"/>
        </div>

        <ol className="mt-3">
          <li><b>เลือกวันที่งวด</b> แล้วกด <b>“รันทำนาย”</b> — ผลจะคงที่สำหรับวันนั้น (deterministic)</li>
          <li><b>ดูเลข Top 5</b> และป้าย <b>Top5 / Top10 / ผลจริง</b> ใต้ผลทำนาย</li>
          <li>เปิด <b>ตารางความน่าจะเป็น</b> และกด <b>“โหลด Heatmap”</b> เพื่อดูค่า Ψ(n)</li>
          <li>กด <b>“รัน Schrödinger”</b> เพื่อดู Top 10 ของเลข 3 หลักที่สุ่มติดบ่อย</li>
          <li>ชอบผลงาน? <b>ทิป 20 บาท</b> ได้ที่ปุ่มด้านบน ☕️</li>
        </ol>

        <div className="mt-3">
          <b>ข้อจำกัด/คำเตือน</b>
          <ul className="mt-2">
            <li>ระบบสร้างขึ้นเพื่อการทดลอง/การศึกษา ไม่รับประกันความถูกต้อง</li>
            <li>การทิปไม่เพิ่มโอกาสถูกรางวัล โปรดใช้วิจารณญาณในการเล่น</li>
          </ul>
        </div>

        <div className="text-end mt-3">
          <button className="btn btn-primary" onClick={onClose}>เข้าใจแล้ว</button>
        </div>
      </div>
    </div>
  );
}
