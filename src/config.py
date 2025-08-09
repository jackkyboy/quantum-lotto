# /Users/apichet/quantum_lotto/src/config.py

# config.py
# config.py
import hashlib
import random
import numpy as np

def generate_seed_from_date(draw_date_str: str) -> int:
    """
    รับค่า date string (เช่น '2025-08-16') แล้วแปลงเป็นค่า SEED (int)
    ใช้ SHA256 เพื่อสร้างค่าที่เสถียรและสม่ำเสมอ
    """
    hash_object = hashlib.sha256(draw_date_str.encode())
    # ใช้ 32-bit เพื่อให้เข้ากันได้กับ NumPy RNG และระบบอื่น ๆ
    seed = int(hash_object.hexdigest(), 16) % (2**32)
    return seed

def lock_seed(seed_value: int):
    """
    ล็อก seed ให้กับทั้ง random และ numpy (global state)
    ⚠ ใช้ได้ แต่ไม่แนะนำถ้าทำงาน multi-thread/multi-request
    """
    random.seed(seed_value)
    np.random.seed(seed_value)
    print(f"🔐 Global Seed ถูกล็อกไว้ที่: {seed_value}")

def make_rngs(seed_value: int):
    """
    สร้าง local RNGs สำหรับทั้ง Python และ NumPy
    ปลอดภัยจากการชนกันของ thread หรือ async request
    """
    py_rng = random.Random(seed_value)           # local Python RNG
    np_rng = np.random.default_rng(seed_value)   # NumPy Generator
    return py_rng, np_rng
