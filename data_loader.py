# /Users/apichet/quantum_lotto/src/data_loader.py
# src/data_loader.py
import os
import json
import pandas as pd
from data.parse_thai_date import parse_thai_date

def load_json_data():
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "lotto_110year_full_fixed.json"))
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # ✅ แปลงวันที่ไทยเป็น datetime
    df["date"] = df["date"].apply(parse_thai_date)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # ✅ เตรียมคอลัมน์เลข 3 หลัก
    digit_cols = ["front3_1", "front3_2", "last3_1", "last3_2", "last3_3"]
    available_cols = [col for col in digit_cols if col in df.columns]
    df["3digits"] = df[available_cols].astype(str).values.tolist()

    # ✅ แตกแถวออกจาก list
    df_expanded = df.explode("3digits").reset_index(drop=True)
    df_expanded["3digits"] = df_expanded["3digits"].astype(str).str.zfill(3)

    # ✅ กรองเฉพาะแถวที่มีวันที่ถูกต้อง
    df_expanded = df_expanded[df_expanded["date"].notna()].copy()

    return df_expanded
