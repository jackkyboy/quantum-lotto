# /Users/apichet/quantum_lotto/src/config.py

# config.py
import hashlib
import random
import numpy as np

def generate_seed_from_date(draw_date_str: str) -> int:
    """
    รับค่า date string (เช่น '2025-08-16') แล้วแปลงเป็นค่า SEED (int)
    """
    # ใช้ hashlib เพื่อแปลง string เป็นตัวเลข
    hash_object = hashlib.sha256(draw_date_str.encode())
    seed = int(hash_object.hexdigest(), 16) % (10**8)  # ตัดให้สั้นลง
    return seed

def lock_seed(seed_value: int):
    """
    ล็อก seed ให้กับทั้ง random และ numpy
    """
    random.seed(seed_value)
    np.random.seed(seed_value)
    print(f"🔐 Seed ถูกล็อกไว้ที่: {seed_value}")
