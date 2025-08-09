# run/run_particle.py

# run/run_particle.py
# run/run_particle.py

from visualizer import (
    plot_particle_field_heatmap,
    most_common_entangled_pairs,
    track_psi_over_time,
    track_actual_psi_over_time
)

from predictors_particle import (
    extract_tail2_digits,
    predict_2digit_particle_field
)

from config import generate_seed_from_date, lock_seed



import pandas as pd
import os
import json


def run_particle_prediction(df, save_image=True, return_plot_path=False):
    past_2digit_results = extract_tail2_digits(df)
    result_df, picks = predict_2digit_particle_field(
        past_2digits=past_2digit_results,
        k=5,
        seed=get_seed()
    )

    latest_draw = df[df["date"].notna()].sort_values("date", ascending=False).iloc[0]
    print(f"\n📅 งวดล่าสุด: {latest_draw['date'].strftime('%d-%m-%Y')} | เลขที่ออก: {latest_draw['last2']}")

    print("\n🎯 ทำนายเลขท้าย 2 ตัวจาก Particle Field:")
    for p in picks:
        print("🔮", p)

    actual_last2 = str(latest_draw["last2"]).zfill(2)
    if actual_last2 in picks:
        print(f"\n✅ ถูก! มีเลข {actual_last2} ในคำทำนาย")
    else:
        print(f"\n❌ ไม่ตรงกับผลจริง ({actual_last2})")

    print("\n🔝 Top 10 Ψ(n):")
    print(result_df.head(10))

    print("\n🧬 คู่ entangled ที่พบบ่อยที่สุด:")
    print(most_common_entangled_pairs(past_2digit_results, top_k=5))

    # ➕ Save CSV
    output_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "particle_field_output.csv"))
    result_df.to_csv(output_csv, index=False)
    print(f"\n📦 บันทึกผลที่: {output_csv}")

    # 📊 Save heatmap image
    image_path = None
    if save_image:
        image_path = plot_particle_field_heatmap(result_df, filename="particle_field_heatmap.png")

    # ✅ ส่งกลับผลลัพธ์ (และ path ถ้าต้องการ)
    if return_plot_path:
        return result_df, picks, image_path
    else:
        return result_df



# ✅ CLI เรียกตรง
# ✅ CLI เรียกตรง
if __name__ == "__main__":
    import sys
    import os
    import json
    import pandas as pd

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    # 📥 โหลดจาก JSON
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "lotto_110year_full_fixed.json"))
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # 👇 ใช้ parser แบบไทยถ้ามี
    from data.parse_thai_date import parse_thai_date
    df["date"] = df["date"].apply(parse_thai_date)

    # 🔧 เตรียมคอลัมน์ "3digits"
    digit_cols = ["front3_1", "front3_2", "last3_1", "last3_2", "last3_3"]
    available_cols = [col for col in digit_cols if col in df.columns]
    df["3digits"] = df[available_cols].astype(str).values.tolist()

    # ✅ explode ให้ตรง index
    df_expanded = df.explode("3digits").reset_index(drop=True)
    df_expanded["3digits"] = df_expanded["3digits"].astype(str).str.zfill(3)

    # 🔁 ป้องกัน date เป็น NaT
    df_expanded = df_expanded[df_expanded["date"].notna()].copy()

    # ✅ เรียกฟังก์ชันหลัก
    if not df_expanded.empty:
        run_particle_prediction(df_expanded)
    else:
        print("❌ ไม่มีข้อมูลวันที่ที่ใช้งานได้ (date = NaT ทั้งหมด)")
