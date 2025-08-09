# src/storage/db.py
# src/storage/db.py
import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# -----------------------------
# ENV & Config
# -----------------------------
# ใช้ DATABASE_URL ถ้ามี (แนะนำสำหรับ Production), ไม่มีก็ fallback SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
DEFAULT_SQLITE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "outputs", "prediction_logs.db")
)
SQLITE_PATH = os.getenv("SQLITE_PATH", DEFAULT_SQLITE_PATH)

# Debug SQL log (0/1)
DEBUG_SQL = os.getenv("DEBUG_SQL", "0") == "1"

# -----------------------------
# Engine
# -----------------------------
engine = None

if DATABASE_URL:
    # รองรับ url แบบ postgres:// ให้แปลงเป็น postgresql+psycopg2://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    # สร้าง engine สำหรับ Postgres (หรือ DB อื่นตาม URL)
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        future=True,
        echo=DEBUG_SQL
    )
else:
    # เตรียมโฟลเดอร์เก็บไฟล์ SQLite
    os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
    engine = create_engine(
        f"sqlite:///{SQLITE_PATH}",
        connect_args={"check_same_thread": False},
        future=True,
        echo=DEBUG_SQL
    )

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

# -----------------------------
# Models
# -----------------------------
class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    draw_date = Column(String, index=True)               # "YYYY-MM-DD"
    model = Column(String, index=True)                   # "particle" | "schrodinger"
    feature = Column(String, default="default")          # "particle_field" | "stochastic" | etc.
    seed = Column(Integer)
    picks = Column(Text)                                 # JSON list
    topn = Column(Text)                                  # JSON list/dict
    actual = Column(String, nullable=True)               # "last2" หรือ "3digits"
    hit = Column(Boolean, default=False)

# -----------------------------
# Init / Utilities
# -----------------------------
def init_db():
    """
    สร้างตาราง (idempotent). ใช้ได้ทั้ง Postgres/SQLite
    """
    Base.metadata.create_all(engine)

def log_prediction(draw_date, model, feature, seed, picks, topn, actual, hit):
    """
    บันทึกผลการทำนายลงฐานข้อมูล
    - picks/topn เก็บเป็น JSON string (Text) เพื่อความเข้ากันได้ทุก DB
    """
    sess = SessionLocal()
    try:
        rec = PredictionLog(
            draw_date=draw_date,
            model=model,
            feature=feature,
            seed=int(seed) if seed is not None else None,
            picks=json.dumps(picks) if picks is not None else "[]",
            topn=json.dumps(topn) if topn is not None else "[]",
            actual=actual,
            hit=bool(hit),
        )
        sess.add(rec)
        sess.commit()
        return rec.id
    finally:
        sess.close()
