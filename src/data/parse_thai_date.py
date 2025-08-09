# src/data/parse_thai_date.py
import re
from datetime import datetime
import pandas as pd

thai_months = {
    "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4,
    "พฤษภาคม": 5, "มิถุนายน": 6, "กรกฎาคม": 7, "สิงหาคม": 8,
    "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
}

def parse_thai_date(text):
    match = re.match(r"(\d{1,2})([ก-๙]+)(\d{4})", str(text))
    if match:
        day, month_th, year_th = match.groups()
        month = thai_months.get(month_th)
        year = int(year_th) - 543
        if month:
            return datetime(year, month, int(day))
    return pd.NaT


# ✅ ทดสอบเฉพาะเวลารันตรง
if __name__ == "__main__":
    sample_dates = [
        "1สิงหาคม2568",
        "16กรกฎาคม2568",
        "2พฤษภาคม2568",
        "31ธันวาคม2567",
        "11เมษายน2560"
    ]

    for d in sample_dates:
        parsed = parse_thai_date(d)
        print(f"{d} → {parsed.strftime('%Y-%m-%d') if pd.notna(parsed) else '❌ ไม่สามารถแปลงได้'}")
