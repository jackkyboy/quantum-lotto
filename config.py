# /Users/apichet/quantum_lotto/src/config.py
# config.py
import hashlib
import random
import numpy as np

# ✅ เก็บ seed ให้โมดูลอื่นเรียกใช้ได้
GLOBAL_SEED: int | None = None

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

def get_seed(default: int | None = None) -> int | None:
    """
    คืนค่า seed ปัจจุบัน (ถ้าไม่เคยล็อกจะคืน default)
    """
    return GLOBAL_SEED if GLOBAL_SEED is not None else default
