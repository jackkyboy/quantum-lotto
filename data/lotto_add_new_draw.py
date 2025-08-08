# 📁 /Users/apichet/quantum_lotto/src/data/lotto_add_new_draw.py
# 📁 src/data/lotto_add_new_draw.py

# 📁 src/data/lotto_add_new_draw_safe.py

import pandas as pd
from datetime import datetime

# ====== 🗂 โหลดข้อมูลเดิม ======
path = "/Users/apichet/quantum_lotto/src/data/lotto_110year.csv"
backup_path = path.replace(".csv", "_backup_before_fix.csv")
df = pd.read_csv(path)

# 🛟 สำรองไฟล์ไว้ก่อน
df.to_csv(backup_path, index=False)
print(f"📦 สำรองข้อมูลไว้ที่: {backup_path}")

# ====== 🆕 ข้อมูลใหม่ ======
new_rows = [
    ["1สิงหาคม2568",  "811852", "52", "852", "501", "42", "525", "512", "891"],
    ["16กรกฎาคม2568", "245324", "24", "324", "261", "71", "995", "084", "336"],
    ["1กรกฎาคม2568",  "949246", "46", "246", "911", "69", "680", "261", "918"],
    ["16มิถุนายน2568", "507392", "92", "392", "060", "17", "243", "299", "736"],
    ["1มิถุนายน2568",  "559352", "52", "352", "201", "34", "349", "044", "307"],
]

columns = [
    "date", "first_prize", "last2", "front3_1", "front3_2",
    "last3_1", "last3_2", "last3_3", "last3_4"
]
new_df = pd.DataFrame(new_rows, columns=columns)

# ====== 🗓 แปลงวันที่ไทยเป็น datetime ======
month_map = {
    "มกราคม": "01", "กุมภาพันธ์": "02", "มีนาคม": "03", "เมษายน": "04",
    "พฤษภาคม": "05", "มิถุนายน": "06", "กรกฎาคม": "07", "สิงหาคม": "08",
    "กันยายน": "09", "ตุลาคม": "10", "พฤศจิกายน": "11", "ธันวาคม": "12"
}

def parse_thai_date(date_str):
    for th, num in month_map.items():
        if th in date_str:
            day = ''.join(filter(str.isdigit, date_str.split(th)[0]))
            year_th = ''.join(filter(str.isdigit, date_str.split(th)[1]))
            return datetime.strptime(f"{int(day):02d}-{num}-{int(year_th)-543}", "%d-%m-%Y")
    return pd.NaT

# เฉพาะ new_df เท่านั้น
new_df["date"] = new_df["date"].apply(parse_thai_date)

# ====== ✨ แปลง date ของ df เดิมให้เป็น datetime (ถ้ามีอยู่แล้ว) ======
if df["date"].dtype == "O":
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ====== 🧠 รวมเฉพาะแถวที่ยังไม่มีในข้อมูลเดิม ======
existing_dates = set(df["date"].dropna())
filtered_new = new_df[~new_df["date"].isin(existing_dates)]

# ====== 🔁 รวมใหม่อย่างปลอดภัย ======
final_df = pd.concat([df, filtered_new], ignore_index=True)
final_df = final_df.sort_values("date")

# ====== 💾 เขียนกลับไฟล์เดิม ======
final_df.to_csv(path, index=False)
print(f"✅ เพิ่มข้อมูลใหม่ {len(filtered_new)} งวด เรียบร้อยแล้ว")
