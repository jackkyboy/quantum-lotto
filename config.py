# /Users/apichet/quantum_lotto/src/config.py
from typing import Optional
import hashlib
import random
import numpy as np
import os

# ✅ เก็บ seed ให้โมดูลอื่นเรียกใช้ได้
GLOBAL_SEED: Optional[int] = None

def generate_seed_from_date(draw_date_str: str) -> int:
    """
    รับค่า date string (เช่น '2025-08-16') แล้วแปลงเป็นค่า SEED (int)
    """
    h = hashlib.sha256(draw_date_str.encode())
    return int(h.hexdigest(), 16) % (10**8)

def lock_seed(seed_value: int):
    """
    ล็อก seed ให้กับทั้ง random และ numpy และบันทึกลง GLOBAL_SEED
    """
    global GLOBAL_SEED
    GLOBAL_SEED = seed_value
    random.seed(seed_value)
    np.random.seed(seed_value)
    print(f"🔐 Seed ถูกล็อกไว้ที่: {seed_value}")

def get_seed(default: Optional[int] = None) -> Optional[int]:
    """
    คืนค่า seed ปัจจุบัน (ถ้าไม่เคยล็อกจะคืน default)
    """
    return GLOBAL_SEED if GLOBAL_SEED is not None else default

# ✅ กำหนดโฟลเดอร์เก็บ output ให้เป็นภายในโปรเจกต์
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# ✅ สร้างโฟลเดอร์ถ้ายังไม่มี
os.makedirs(OUTPUT_DIR, exist_ok=True)
